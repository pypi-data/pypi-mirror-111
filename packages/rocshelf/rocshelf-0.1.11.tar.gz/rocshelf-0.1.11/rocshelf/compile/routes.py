""" Модуль компиляции страниц.

Компиляция зависит от следующих параметров:
    Маршруты (настройка route): каждый маршрут - это отдельная страница
    Файлы локализации (настройка path -> import -> localization):
        На каждый файл с расширением .lang будет производиться итерация компиляция страниц из пункта выше.
        Результат компиляции каждого файла локализации будет храниться в папке с именем файла локализации.

"""

from __future__ import annotations

import multiprocessing as _M
import typing as _T
import rlogging
from bs4 import BeautifulSoup
from rcore import sync
from rocshelf import template
from rocshelf.compile import params, tracebacks, controller
from rocshelf.components import localization
from rocshelf.components.relations import Relation
from rocshelf.components.routes import GetRoute
from rocshelf.frontend.chunks import Chunk

logger = rlogging.get_logger('mainLogger')

PROCESSING_PARSE_SHELVES_CACHE_FILE = 'rocshelf-used-shelves.json'


@tracebacks.stage_pre_analyze
def pre_analyze():
    """ Запуск анализатора шаблонов.

    Нужен для прочтения всех файлов, разбитие их на литералы и предварительную обработку.

    """

    logger.info('Анализ всех используемых shelf-страниц')

    for routeKey, route in GetRoute.walk():
        logger.debug('Анализ shelf-страницы "{0}" на которую ссылается маршрут "{1}"'.format(
            route.page,
            routeKey
        ))

        template.shelves.ShelfPageNode(route.page)


class CompileRoute(sync.process.OnProcessMixin):
    """ Класс в рамках которого происходит компиляция одного маршрута для одной локации """

    localizationName: str
    routeKey: str

    inputQueue: _M.Queue
    outputQueue: _M.Queue

    relation: Relation

    procParams: params.ProcessingParams

    def __init__(self, localizationName: str, routeKey: str, inputQueue: _M.Queue, outputQueue: _M.Queue):
        self.localizationName = localizationName
        self.routeKey = routeKey

        self.inputQueue = inputQueue
        self.outputQueue = outputQueue

        self.relation = Relation(None, localizationName)

        self.procParams = params.TemplateCompilationMetaData.processing_params(routeKey, localizationName)

    @tracebacks.stage_route_processing
    def processing(self, shelfNode: template.shelves.ShelfPageNode) -> template.nodes.ProcessingOutputNode:
        """ Обработка маршрута

        Args:
            shelfNode (template.shelves.ShelfPageNode): Узел shelf-страницы

        Returns:
            template.nodes.ProcessingOutputNode: Узел результата обработки

        """

        logger.info('Обработка маршрута "{0}" с локализацией "{1}"'.format(
            self.routeKey, self.localizationName
        ))

        return shelfNode.processing(self.procParams)

    def processing_data_analyze(self, processingNode: template.nodes.ProcessingOutputNode):
        """ Передача данных, собранных во время обработки, в соответствующие модули.

        Args:
            processingNode (template.nodes.ProcessingOutputNode): Узел результата обработки

        """

        # Передача в процесс-контроллер собраных данных
        self.inputQueue.put(processingNode.collectedData)

        # Получение результата котроллера
        # chunks - список чанков компилируемого маршрута
        chunks: list[Chunk] = self.outputQueue.get()

        # Добавление чанков в процесс компиляции
        self.procParams.meta().add_chucks(chunks)

    @tracebacks.stage_route_compile
    def compile(self, processingNode: template.nodes.ProcessingOutputNode) -> str:
        """ Компиляция маршрута

        Args:
            processingNode (template.nodes.ProcessingOutputNode): Узел результата обработки

        Returns:
            str: Скомпилированный текст

        """

        logger.info('Компиляция маршрута "{0}" в локализации "{1}"'.format(
            self.routeKey, self.localizationName
        ))

        return processingNode.compile(self.procParams)

    def save(self, compiledText: str):
        """ Сохранение результата компиляции

        Args:
            compiledText (str): Текст - результат компиляции

        """

        logger.info('Сохранение результата компиляции маршрута "{0}" в локализации "{1}"'.format(
            self.routeKey, self.localizationName
        ))

        filePath = self.relation.template_path(self.routeKey)
        if not filePath.check():
            filePath.create()

        filePath.write(compiledText, 'w')

    def normalize_html(self):
        """ Нормализация html разметки скомпилированного файла """

        pageFile = self.relation.template_path(self.routeKey)

        logger.debug('Нормализация Html страницы "{0}" маршрута "{1}" в локализации "{2}"'.format(
            pageFile, self.routeKey, self.localizationName
        ))

        pageText = pageFile.read()

        soup = BeautifulSoup(pageText, 'html.parser')

        pageText = soup.prettify()

        pageFile.write(pageText, 'w')

    @tracebacks.stage_route
    def on_process(self):
        page = GetRoute.route(self.routeKey).page
        shelfNode = template.shelves.ShelfPageNode(page)
        processingNode = self.processing(shelfNode)
        self.processing_data_analyze(processingNode)
        compiledText = self.compile(processingNode)
        self.save(compiledText)
        self.normalize_html()


class CompileLocalization(sync.process.OnProcessMixin):
    """ Класс в рамках которого происходит компиляция всех маршрутов для одной локации """

    localizationName: _T.Optional[str]

    def __init__(self, localizationName: _T.Optional[str] = None) -> None:
        self.localizationName = localizationName

    def start(self, controllerManager: controller.CompileLocalizationController):
        """ Запуск компиляции маршрутов некой локализации

        Args:
            controllerManager (CompileLocalizationController): Менеджер контроллера, который синхронизирует компиляцию маршрутов

        """

        routes = GetRoute.list()

        logger.info('Запуск паралельной компиляции маршрутов в локализации "{0}" в {1} процессах'.format(
            self.localizationName, len(routes)
        ))

        processesPool = sync.process.NoDeamonProcessesPoolController(CompileRoute)

        for routeKey in routes:
            inputQueue, outputQueue = controllerManager.queues(routeKey)
            processesPool.add_process(self.localizationName, routeKey, inputQueue, outputQueue)

        processesPool.map()

    @tracebacks.stage_localization
    def on_process(self):
        compileController = controller.CompileLocalizationController(self.localizationName, GetRoute.list())

        with compileController as controllerManager:
            self.start(controllerManager)


def run():
    """ Запуск компиляции маршрутов """

    logger.info('Компиляция маршрутов. Компиляция будет происходить параллельно для {0} локализаций'.format(
        len(localization.localsData)
    ))

    processesPool = sync.process.NoDeamonProcessesPoolController(CompileLocalization)

    for localizationName in localization.GetLocal.all():
        processesPool.add_process(localizationName)

    processesPool.map()

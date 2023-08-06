""" Модуль описания контроллеров, которые следят за процессом компиляции """

import json
import typing as _T

import rlogging
from rcore.rpath import rPath
from rocshelf.compile import static
from rocshelf.frontend.chunks import Chunk, StaticAnalyze
from rcore.sync import controllers

saveStaticChunksFileName = 'rocshelf-static-chunks.json'

logger = rlogging.get_logger('mainLogger')


class CompileLocalizationControllerWorker(controllers.workers.BaseControllerWorker):
    """ Worker котроллера для управления процессом компиляции маршрутов для некой локализации """

    localizationName: str
    routes: list[str]

    def __init__(self, localizationName: str, routes: list[str]) -> None:
        self.localizationName = localizationName
        self.routes = routes

    def put_data(self, chunks: list[Chunk]):
        """ Отправка обработанных данных в очереди

        Args:
            chunks (list[Chunk]): Список чанков

        """

        outputtedData = {}

        for routeKey in self.routes:
            outputtedData[routeKey] = [chunk for chunk in chunks if routeKey in chunk.routeKeys]

        super().put_data(outputtedData)

    def worker(self):
        logger.info('Запущен worker контроллера "{0}" для локализации "{1}"'.format(
            self.__class__.__name__, self.localizationName
        ))

        collectedData = self.get_data()

        chunks = self.analyze_static(collectedData)
        self.save_cache(chunks)
        self.compile_static(chunks)

        self.put_data(chunks)

    def analyze_static(self, collectedData: dict[str, _T.Any]) -> list[Chunk]:
        """ Передача собраных данных в анализатор статики

        Args:
            collectedData (dict[str, _T.Any]): Собранные данные

        Returns:
            list[Chunk]: Результат обработки статики. Список чанков

        """

        logger.info('Передача собраных, во время компиляции маршутов в локализации "{0}", данных в анализатор статики'.format(
            self.localizationName
        ))

        staticProcessingData = {
            'shelves': {}
        }

        for routeKey in self.routes:
            staticProcessingData['shelves'][routeKey] = set(collectedData[routeKey]['shelves'])

        staticAnalyze = StaticAnalyze.all_stages(
            staticProcessingData
        )

        return staticAnalyze.chunks

    def save_cache(self, chunks: list[Chunk]):
        """ Сохранение результатов анализа в кеш

        Args:
            chunks (list[Chunk]): Чанки статики

        """

        filePath = rPath(saveStaticChunksFileName, fromPath='cache')

        dump = {}

        if filePath.check():
            dump = json.loads(filePath.read())
            if not isinstance(dump, dict):
                dump = {}

        dump[self.localizationName] = []

        for chuck in chunks:
            dump[self.localizationName].append({
                'routes': list(chuck.routeKeys),
                'shelves': list(chuck.shelfSlugs)
            })

        filePath.write(json.dumps(dump, indent=4), 'w')

    def compile_static(self, chunks: list[Chunk]):
        """ Запуск компиляции статики

        Args:
            chunks (list[Chunk]): Чанки статики

        """

        logger.debug('Запуск компиляции статики из контроллера "{0}" в локализации "{1}" чанков: {2}'.format(
            self.__class__.__name__,
            self.localizationName,
            chunks
        ))

        static.start_compile(
            self.localizationName,
            chunks
        )


class CompileLocalizationController(controllers.BaseController):
    """ Котроллер для управления процессом компиляции маршрутов для некой локализации """

    workerClass = CompileLocalizationControllerWorker

    def __init__(self, localizationName: str, routesList: list[str]) -> None:
        super().__init__(localizationName, routesList)

        self.generate_queues(routesList)

    def generate_queues(self, routesList: list[str]):
        """ Заполнение словарей очередей для input и output

        Args:
            routesList (list[str]): Список компилируемых маршуртов

        """

        for routeKey in routesList:
            self.manager.set_queues(routeKey)

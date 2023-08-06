""" Модуль описания контроллеров, которые следят за процессом компиляции """

from rcore.rpath import rPath
import multiprocessing as _M
import typing as _T
from multiprocessing.managers import SyncManager
import json
import rlogging
from rocshelf.compile import static
from rocshelf.frontend.chunks import Chunk, StaticAnalyze

saveStaticChunksFileName = 'rocshelf-static-chunks.json'

logger = rlogging.get_logger('mainLogger')


class BaseControllerWorker(object):
    """ Базовый worker класс, который осуществляет контроллерскую работы """

    inputtedQueue: dict[str, _M.Queue]
    outputtedQueue: dict[str, _M.Queue]
    commonQueue: _M.Queue

    def target(self, inputtedQueue: dict[str, _M.Queue], outputtedQueue: dict[str, _M.Queue], commonQueue: _M.Queue) -> None:
        self.inputtedQueue = inputtedQueue
        self.outputtedQueue = outputtedQueue
        self.commonQueue = commonQueue

        self.worker()

    def worker(self):
        """ Функция, которая будет запускаться в новом процессе """

    def put_data(self, outputtedData: dict[str, _T.Any]):
        """ Выдача результатов обработки

        Args:
            outputtedData (dict[str, _T.Any]): Данные для выдачи

        """

        for processKey, processOutputQueue in self.outputtedQueue.items():
            processOutputQueue.put(outputtedData[processKey])


class BaseController(object):
    """ Базовый класс интерфейса для обмена сообщениями между контроллером и процессами """

    manager: SyncManager
    inputtedQueue: dict[str, _M.Queue]
    outputtedQueue: dict[str, _M.Queue]
    commonQueue: _M.Queue

    workerClass: type[BaseControllerWorker]
    worker: BaseControllerWorker

    process: _M.Process

    def __init__(self, *args, **kwargs):
        """ Инициализация контроллера.

        Переданные параметры будут переданы в инициализацию workerClass.

        Args:
            args (tuple): Параметры инициализации workerClass.
            kwargs (dict): Параметры инициализации workerClass.

        """

        self.manager = _M.Manager()

        self.inputtedQueue = {}
        self.outputtedQueue = {}
        self.commonQueue = self.manager.Queue(0)

        self.worker = self.workerClass(*args, **kwargs)

    def start_worker(self):
        """ Запуск worker процесса """

        self.process = _M.Process(target=self.worker.target, args=(self.inputtedQueue, self.outputtedQueue, self.commonQueue))
        self.process.start()

    def stop_worker(self):
        """ Остановка worker процесса """

        self.process.join()
        self.process.terminate()

    def queues(self, processKey: str):
        return self.inputtedQueue[processKey], self.outputtedQueue[processKey]

    def common(self):
        """ Получение общей информации об обработанных контроллером данных """

        return self.commonQueue.get()


class CompileLocalizationControllerWorker(BaseControllerWorker):
    """ Worker котроллера для управления процессом компиляции маршрутов для некой локализации """

    localizationName: str
    routes: list[str]

    def __init__(self, localizationName: str, routes: list[str]) -> None:
        self.localizationName = localizationName
        self.routes = routes

    def get_data(self) -> dict[str, _T.Any]:
        """ Получение данных из очередей

        Returns:
            dict[str, _T.Any]: Словарь процессов и их данных

        """

        inputtedData: dict[str, _T.Any] = {}

        for routeKey, queue in self.inputtedQueue.items():
            inputtedData[routeKey] = queue.get()

        return inputtedData

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
        self.commonQueue.put(chunks)

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

        dump = []

        for chuck in chunks:
            dump.append({
                'routes': list(chuck.routeKeys),
                'shelves': list(chuck.shelfSlugs)
            })

        filePath.write(json.dumps(dump), 'w')

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


class CompileLocalizationController(BaseController):
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
            self.inputtedQueue[routeKey] = self.manager.Queue(1)
            self.outputtedQueue[routeKey] = self.manager.Queue(1)

import multiprocessing as _M
import typing as _T
from rcore.sync.controllers import managers


class BaseControllerWorker(object):
    """ Базовый worker класс, который осуществляет контроллерскую работы """

    manager: managers.BaseControllerManager

    def target(self, manager: managers.BaseControllerManager) -> None:
        self.manager = manager

        self.worker()

    def worker(self):
        """ Функция, которая будет запускаться в новом процессе """

    def get_data(self) -> dict[str, _T.Any]:
        """ Получение данных из очередей

        Returns:
            dict[str, _T.Any]: Словарь процессов и их данных

        """

        inputtedData: dict[str, _T.Any] = {}

        for routeKey, queue in self.manager.inputtedQueue.items():
            inputtedData[routeKey] = queue.get()

        return inputtedData

    def put_data(self, outputtedData: dict[str, _T.Any]):
        """ Выдача результатов обработки

        Args:
            outputtedData (dict[str, _T.Any]): Данные для выдачи

        """

        for processKey, processOutputQueue in self.manager.outputtedQueue.items():
            processOutputQueue.put(outputtedData[processKey])

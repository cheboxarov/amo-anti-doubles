from abc import ABC, abstractmethod


class AbstractLogger(ABC):

    @abstractmethod
    def send_log(self, message: str): pass
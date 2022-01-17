from abc import ABC
from abc import abstractmethod


class Logger(ABC):
    @abstractmethod
    def log_exception(self, exception: Exception) -> None:
        ...

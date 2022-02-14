from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def log_exception(self, exception: Exception) -> None:
        ...

from paper_tactics.ports.logger import Logger


class StdoutLogger(Logger):
    def log_exception(self, exception: Exception):
        print(repr(exception))

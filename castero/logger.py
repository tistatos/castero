import socket


class UDPLogger:
    """Logger method that print all log messages to an host on port with UDP
    """
    def __init__(self, host, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._destination = (host, port)

    def close(self):
        self._socket.close()

    def write(self, message):
        self._socket.sendto(bytes(message + '\n', 'utf-8'), self._destination)


class FileLogger:
    """Logger method that print all log messages to file.
    TODO: avoid creating large log files by creating a new file if the current
    file is too big
    """
    def __init__(self, filename):
        self._filename = filename

    def close(self):
        pass

    def write(self, message):
        with open(self._filename, 'a') as f:
            f.write(message + '\n')


class Logger:
    ERROR = -2
    WARNING = -1
    INFO = 0
    DEBUG = 1
    TRACE = 2
    METHOD = None

    LOG_LEVEL = 0

    class NullLogger:
        """Class with no side effects if logging is disabled
        """
        def __init__(self):
            pass

        def close(self):
            pass

        def write(self, message):
            pass

    @staticmethod
    def start(method=NullLogger(), log_level=INFO):
        Logger.METHOD = method
        Logger.LOG_LEVEL = log_level

    @staticmethod
    def close():
        Logger.METHOD.close()

    @staticmethod
    def error(message):
        if Logger.LOG_LEVEL >= Logger.ERROR:
            Logger.METHOD.write(message)

    @staticmethod
    def warning(message):
        if Logger.LOG_LEVEL >= Logger.WARNING:
            Logger.METHOD.write(message)

    @staticmethod
    def info(message):
        if Logger.LOG_LEVEL >= Logger.INFO:
            Logger.METHOD.write(message)

    @staticmethod
    def debug(message):
        if Logger.LOG_LEVEL >= Logger.DEBUG:
            Logger.METHOD.write(message)

    @staticmethod
    def trace(message):
        if Logger.LOG_LEVEL >= Logger.TRACE:
            Logger.METHOD.write(message)

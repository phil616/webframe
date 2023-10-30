"""
    core.logger.py
    ~~~~~~~~~
    日志体系
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""
import logging
import logging.handlers
from os import mkdir
from os.path import join, dirname, abspath, exists


LOG_normal_format = ("[ %(levelname)s ] %(asctime)s %(filename)s:%(lineno)d %(message)s")
LOG_debug_format = ("[ %(levelname)s ] %(threadName)s %(asctime)s %(filename)s:%(lineno)d %(message)s")


class Logger(object):
    def __init__(self, logname, active_uvicorn: bool = True, LEVEL: str = "debug", backup_count: int = 10):
        self._syslog = None
        self.logname = logname
        self.log_dir = join(dirname(dirname(abspath(__file__))), "logs")
        self.log_file = join(self.log_dir, "{0}.log".format(self.logname))

        self._levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        self._logfmt = "%Y-%m-%d %H:%M:%S"
        self._logger = logging.getLogger(self.logname)
        if not exists(self.log_dir):
            mkdir(self.log_dir)
        LEVEL = LEVEL.upper()
        if LEVEL == "DEBUG":
            LOGFMT = LOG_debug_format
        else:
            LOGFMT = LOG_normal_format
        handler = logging.handlers.TimedRotatingFileHandler(
            filename=self.log_file, backupCount=backup_count, when="midnight"
        )
        handler.suffix = "%Y%m%d"
        self.formatter = logging.Formatter(LOGFMT, datefmt=self._logfmt)
        handler.setFormatter(self.formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self._levels.get(LEVEL))
        stream_handler.setFormatter(self.formatter)
        self._logger.addHandler(handler)
        self._logger.addHandler(stream_handler)
        self._logger.setLevel(self._levels.get(LEVEL))
        self.level = LEVEL
        #  uvicorn access api logger
        if active_uvicorn:
            _system_handler = logging.handlers.TimedRotatingFileHandler(
                filename=join(self.log_dir, "{0}.api.log".format("uvicorn_runtime")),
                backupCount=backup_count,
                when="midnight",
            )
            _system_handler.setFormatter(self.formatter)
            _system_handler.setLevel(self._levels.get(self.level))
            self._sys_access_log = logging.getLogger("uvicorn.access")
            self._sys_access_log.addHandler(_system_handler)
            self._sys_error_log = logging.getLogger("uvicorn.error")
            self._sys_error_log.addHandler(_system_handler)
            self._sys_asgi_log = logging.getLogger("uvicorn.asgi")
            self._sys_asgi_log.addHandler(_system_handler)

    @property
    def getLogger(self):
        return self._logger

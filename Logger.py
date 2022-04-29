import logging


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    blue = '\u001b[34m'
    format = "[%(levelname)s]: %(asctime)s - %(message)s "

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: blue + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Logger:
    def custom_logger(self):
        log = logging.getLogger('CarParserLogger')
        if not log.handlers:
            log.setLevel(logging.DEBUG)
            file = logging.FileHandler(filename='CarParserLogger.log', mode='a')
            console = logging.StreamHandler()

            file.setLevel(logging.WARNING)
            console.setLevel(logging.DEBUG)

            file.setFormatter(logging.Formatter('%(levelname)s: %(asctime)s: %(message)s: %(process)d: %(processName)s',
                                                datefmt='%d/%m  %H:%M:%S'))
            console.setFormatter(CustomFormatter())

            log.addHandler(file)
            log.addHandler(console)

        return log

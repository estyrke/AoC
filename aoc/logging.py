import logging
from yachalk import chalk


class CustomFormatter(logging.Formatter):
    format_str = "%(asctime)s %(message)s"

    FORMATS = {
        logging.DEBUG: chalk.gray(format_str),
        logging.INFO: chalk.white(format_str),
        logging.WARNING: chalk.yellow(format_str),
        logging.ERROR: chalk.red(format_str),
        logging.CRITICAL: chalk.bold.red(format_str),
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
        return formatter.format(record)


def init_logging(level=logging.INFO):
    # create logger with 'spam_application'
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(CustomFormatter())

    root_logger.addHandler(ch)


getLogger = logging.getLogger

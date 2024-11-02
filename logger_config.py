import logging
from logging.handlers import TimedRotatingFileHandler
import colorlog


def configure_logger():
    logger = logging.getLogger("krc_logger")
    logger.setLevel(logging.INFO)

    logfile = "mqtt.log"
    # Create file handler and set level to debug
    file_handler = TimedRotatingFileHandler(
        logfile, 
        when="midnight", 
        interval=1, 
        backupCount=7)

    # Create console handler
    console_handler = logging.StreamHandler()

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    # Create formatter for console handler with colors
    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "yellow",
            "WARNING": "blue",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )
    # Add formatter to ch
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(console_formatter)

    # Add ch to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Configure and get the logger
logger = configure_logger()

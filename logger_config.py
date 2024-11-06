import logging
from logging.handlers import TimedRotatingFileHandler
import colorlog
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from config import DATABASE_CONNECTION_STRING

Base = declarative_base()

class LogRecord(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String)
    level = Column(String)
    message = Column(Text)

class DatabaseLogHandler(logging.Handler):
    def __init__(self, db_url):
        super().__init__()
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def emit(self, record):
        session = self.Session()
        log_record = LogRecord(
            timestamp=datetime.datetime.utcnow(),
            name=record.name,
            level=record.levelname,
            message=record.getMessage()
        )
        session.add(log_record)
        session.commit()
        session.close()

class WarningErrorCriticalFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.WARNING, logging.ERROR, logging.CRITICAL)

def configure_logger():
    logger = logging.getLogger("krc_logger")
    logger.setLevel(logging.INFO)

    logfile = "mqtt.log"
    # Create file handler and set level to debug
    file_handler = TimedRotatingFileHandler(
        logfile, 
        when="midnight", 
        interval=1, 
        backupCount=7
    )

    # Create console handler
    console_handler = logging.StreamHandler()

    # Create database handler
    # db_handler = DatabaseLogHandler(DATABASE_CONNECTION_STRING)
    # db_handler.setLevel(logging.WARNING)
    # db_handler.addFilter(WarningErrorCriticalFilter())

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

    # Add formatter to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(console_formatter)
    # db_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    # logger.addHandler(db_handler)

    return logger

# Configure and get the logger
logger = configure_logger()
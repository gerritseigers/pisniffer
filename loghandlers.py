from models.model import Base, LogRecord
from session_config import session
import logging
import datetime

class DatabaseLogHandler(logging.Handler):
    def __init__(self, db_url):
        self.Session = session

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
        return record.levelno in (logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)        
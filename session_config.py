from logger_config import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.model import Base
from config import DATABASE_CONNECTION_STRING

def configure_session():

    logger.info("Configuring session...")
    connection = "sqlite+pysqlite:///demo.db"
    engine = create_engine(DATABASE_CONNECTION_STRING, echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    return Session()


# Configure and get the logger
session = configure_session()
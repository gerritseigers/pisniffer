from logger_config import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.model import Base


def configure_session():

    logger.info("Configuring session...")
    connection = "sqlite+pysqlite:///demo.db"
    engine = create_engine(connection, echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    return Session()


# Configure and get the logger
session = configure_session()
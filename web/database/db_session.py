import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec
import logging
from sqlalchemy.orm import Session

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(logger: logging.Logger,
                db_host: str,
                db_port: int,
                db_login: str,
                db_password: str,
                db_name: str) -> None:
    global __factory

    if __factory:
        return

    conn_str = f'postgresql+psycopg2://{db_login}:{db_password}@{db_host}:{db_port}/{db_name}'
    logger.info(f"Connecting to the database...")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
import logging
from contextlib import contextmanager

from sqlalchemy.engine import Engine, create_engine, Connection
from sqlalchemy.orm import Session, sessionmaker
from starlette.config import Config

from app import config

LOGGER = logging.getLogger(__name__)


class Database(object):
    def __init__(self) -> None:
        super().__init__()
        self.__show_sql = True

    def __call__(self, *args, **kwargs) -> Session:
        session_maker: sessionmaker = self.get_session_maker
        return session_maker()

    def test_connection(self):
        engine: Engine = self.get_engine
        try:
            engine.execute('SELECT 1')
        except Exception as ex:
            raise ValueError('Can\'t connect to ' + str(engine.url))

    @contextmanager
    def connect(self) -> Connection:
        """Provide a transactional scope around a series of operations."""
        conn = self.get_engine.connect()
        try:
            yield conn
        except Exception as ex:
            raise ex
        finally:
            conn.close()

    @contextmanager
    def session(self) -> Session:
        """Provide a transactional scope around a series of operations."""
        session: Session = self.get_session_maker()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    @property
    def get_db_url(self) -> str:
        # This need to be implemented
        return config.SQLALCHEMY_DATABASE_URI

    @property
    def get_engine(self) -> Engine:
        engine = create_engine(self.get_db_url, echo=self.__show_sql)
        return engine

    @property
    def get_session_maker(self) -> sessionmaker:
        return sessionmaker(autocommit=False, bind=self.get_engine, expire_on_commit=False)
    

db = Database()
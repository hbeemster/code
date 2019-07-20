# pylint: disable=attribute-defined-outside-init
import abc
from typing import Callable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from src.allocation import config
from src.allocation import repository


class AbstractUnitOfWork(abc.ABC):

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    def init_repositories(self, batches: repository.AbstractRepository):
        self._batches = batches

    @property
    def batches(self) -> repository.AbstractRepository:
        return self._batches



DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(
    config.get_postgres_uri(),
))

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session = session_factory()  # type: Session
        self.init_repositories(repository.SqlAlchemyRepository(self.session))

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


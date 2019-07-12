import abc
import model


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference):
        raise NotImplementedError



class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def add(self, batch):
        pass

    def get(self, reference) -> model.Batch:
        pass

"""Module for repository factory.
"""

from abc import ABC, abstractmethod
from .abstract_repository import AbstractRepository
from .sqlite_repository import SQLiteRepository


class AbsRepoFactory(ABC):
    """Represents abstract repository factory.
    """
    @abstractmethod
    def get(self, cls: type) -> AbstractRepository:
        """Returns AbstractRepository
        """


class RepositoryFactory(AbsRepoFactory):
    """Represents sqlite repository factory.
    """
    def get(self, cls: type) -> AbstractRepository:
        """Returns repository.

        Args:
            cls (type): type to construct proper repository.

        Returns:
            AbstractRepository: repository.
        """
        return SQLiteRepository[cls]("databases/ui_client.db", cls)


from .sqlite_repository import SQLiteRepository


class RepositoryFactory:
    def get(self, cls):
        return SQLiteRepository[cls]("databases/ui_client.db", cls)
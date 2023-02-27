"""
Простой тестовый скрипт для терминала
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.cats_for_simple_clients import run_bookkeeper

cat_repo = MemoryRepository[Category]()
exp_repo = MemoryRepository[Expense]()

run_bookkeeper(cat_repo, exp_repo)

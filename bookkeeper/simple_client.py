"""
Простой тестовый скрипт для терминала, запускающего репозиторий,
который работает в оперативной памяти
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.run_simple_client import run_simple_client

cat_repo: MemoryRepository[Category] = MemoryRepository()
exp_repo: MemoryRepository[Expense] = MemoryRepository()
bud_repo: MemoryRepository[Budget] = MemoryRepository()

run_simple_client(cat_repo, exp_repo, bud_repo)

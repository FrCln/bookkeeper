"""
Простой тестовый скрипт для терминала
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.cats_for_simple_clients import run_bookkeeper


cat_repo = SQLiteRepository('budget.db', Category)
exp_repo = SQLiteRepository('budget.db', Expense)

run_bookkeeper(cat_repo, exp_repo)

"""
Простой тестовый скрипт для терминала, запускающего репозиторий,
который работает с SQLite
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.run_simple_client import run_simple_client

cat_repo = SQLiteRepository('budget.db', Category)
exp_repo = SQLiteRepository('budget.db', Expense)
bud_repo = SQLiteRepository('budget.db', Budget)

run_simple_client(cat_repo, exp_repo, bud_repo)

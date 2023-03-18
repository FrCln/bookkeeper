import sys

import pytest
from PySide6 import QtWidgets

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.view.view import View


@pytest.fixture
def destroy_app():
    if QtWidgets.QApplication.instance():
        QtWidgets.QApplication.instance().shutdown()


@pytest.fixture
def get_bool_callback():
    def callback(*arg) -> None:
        callback.val = True

    return callback


@pytest.fixture
def get_bool_callback2():
    def callback(*arg) -> None:
        callback.val = True

    return callback


@pytest.fixture
def get_bool_callback3():
    def callback(*arg) -> None:
        callback.val = True

    return callback


@pytest.fixture
def cat_repo():
    repo = MemoryRepository()
    [repo.add(Category(name=f"cat{i}")) for i in range(5)]
    return repo


@pytest.fixture
def exp_repo():
    repo = MemoryRepository()
    [repo.add(Expense(category=i + 1, amount=i)) for i in range(5)]
    return repo


@pytest.fixture
def budget_repo():
    repo = MemoryRepository()
    repo.add(Budget(period="day", total=100))
    repo.add(Budget(period="week", total=500))
    repo.add(Budget(period="month", total=10000))
    return repo


def test_set_categories(destroy_app, cat_repo, get_bool_callback, get_bool_callback2):
    view = View()

    view.expense_add.set_categories = get_bool_callback
    view.expense_table.set_categories = get_bool_callback2

    view.set_categories(cat_repo.get_all())

    assert get_bool_callback.val
    assert get_bool_callback2.val


def test_set_cat_edit_open_callback(destroy_app, get_bool_callback):
    view = View()

    view.expense_add.set_new_window_callback = get_bool_callback
    view.set_cat_edit_open_callback(lambda: None)

    assert get_bool_callback.val


def test_set_cat_edit_save_callback(destroy_app, get_bool_callback):
    view = View()

    view.category_window.set_save_callback = get_bool_callback
    view.set_cat_edit_save_callback(lambda a: None)

    assert get_bool_callback.val


def test_set_cat_text(destroy_app, get_bool_callback):
    view = View()

    view.category_window.set_text = get_bool_callback
    view.set_cat_text("test")

    assert get_bool_callback.val


def test_set_expenses(destroy_app, exp_repo, get_bool_callback):
    view = View()

    view.expense_table.set_expenses = get_bool_callback

    view.set_expenses(exp_repo.get_all())

    assert get_bool_callback.val


def test_set_exp_add_callback(destroy_app, get_bool_callback):
    view = View()

    view.expense_add.set_exp_add_callback = get_bool_callback
    view.set_exp_add_callback(lambda a, b: None)

    assert get_bool_callback.val


def test_set_exp_table_changed_callback(destroy_app, get_bool_callback):
    view = View()

    view.expense_table.set_exp_table_changed_callback = get_bool_callback
    view.set_exp_table_changed_callback(lambda a, b, c: None)

    assert get_bool_callback.val


def test_set_budget(destroy_app, budget_repo, get_bool_callback):
    view = View()

    view.budget_table.set_budget = get_bool_callback

    view.set_budget(budget_repo.get_all())

    assert get_bool_callback.val


def test_set_budget_table_changed_callback(destroy_app, get_bool_callback):
    view = View()

    view.budget_table.set_budget_table_changed_callback = get_bool_callback
    view.set_budget_table_changed_callback(lambda a, b, c: None)

    assert get_bool_callback.val


def test_show_category_edit_window(destroy_app, get_bool_callback):
    view = View()

    view.category_window.show = get_bool_callback

    view.show_category_edit_window()

    assert get_bool_callback.val


def test_run(destroy_app, get_bool_callback, get_bool_callback2, get_bool_callback3):
    view = View()

    view.main_window.show = get_bool_callback
    view.app.exec = get_bool_callback2
    sys.exit = get_bool_callback3

    view.run()

    assert get_bool_callback.val
    assert get_bool_callback2.val
    assert get_bool_callback3.val

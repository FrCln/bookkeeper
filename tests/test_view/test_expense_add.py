import pytest
from pytestqt.qt_compat import qt_api

from bookkeeper.models.category import Category
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.view.expense_add import ExpenseAddBox


@pytest.fixture
def get_callback():
    def callback(val1: str, val2: str) -> None:
        callback.val1 = val1
        callback.val2 = val2

    return callback


@pytest.fixture
def get_window_callback():
    def callback() -> None:
        callback.called = True

    return callback


@pytest.fixture
def cat_repo():
    repo = MemoryRepository()
    [repo.add(Category(name=f"cat{i}")) for i in range(5)]
    return repo


def test_set_exp_add_callback(qtbot, get_callback):
    widget = ExpenseAddBox()
    qtbot.addWidget(widget)

    widget.set_exp_add_callback(get_callback)

    assert get_callback == widget.self_layout.add_button_callback


def test_set_categories(qtbot, cat_repo):
    widget = ExpenseAddBox()
    qtbot.addWidget(widget)

    widget.set_categories(cat_repo.get_all())

    data = [cat.name for cat in cat_repo.get_all()]

    for i in range(widget.self_layout.category.count()):
        assert data[i] == widget.self_layout.category.itemText(i)


def test_button_click(qtbot, get_callback):
    widget = ExpenseAddBox()
    qtbot.addWidget(widget)

    price = "100"

    widget.self_layout.price.setText(price)
    widget.set_exp_add_callback(get_callback)
    qtbot.mouseClick(widget.self_layout.add_button, qt_api.QtCore.Qt.MouseButton.LeftButton)

    assert get_callback.val1 == widget.self_layout.price.text()
    assert get_callback.val2 == widget.self_layout.category.currentText()


def test_new_window_callback(qtbot, get_window_callback):
    widget = ExpenseAddBox()
    qtbot.addWidget(widget)

    widget.set_new_window_callback(get_window_callback)
    qtbot.mouseClick(widget.self_layout.category_edit, qt_api.QtCore.Qt.MouseButton.LeftButton)

    assert get_window_callback.called

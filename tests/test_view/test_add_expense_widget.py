"""
Здесь содержатся тесты для виджета добавления расходов
"""
import pytest

from PyQt6.QtCore import Qt
from pytestqt.qtbot import QtBot

from bookkeeper.view.add_expense_widget import AddExpenseWidget


@pytest.fixture
def widget(qtbot: QtBot) -> AddExpenseWidget:
    widget = AddExpenseWidget()
    qtbot.addWidget(widget)
    return widget


def test_add_expense(qtbot: QtBot, widget: AddExpenseWidget):
    date_input = widget.date_edit
    description_input = widget.description_edit
    category_input = widget.category_combo
    amount_input = widget.amount_edit
    add_button = widget.add_button

    qtbot.keyClicks(date_input, "2022-03-10")
    qtbot.keyClicks(description_input, "DragonBall")
    category_input.setCurrentIndex(0)
    qtbot.keyClicks(amount_input, "12.99")

    with qtbot.waitSignal(widget.expense_added, timeout=1000) as signal:
        qtbot.mouseClick(add_button, Qt.MouseButton.LeftButton)

    assert signal.args == ["2022-03-10", "DragonBall", "Еда", 12.99]

    assert date_input.text() == ""
    assert description_input.text() == ""
    assert amount_input.text() == ""
    assert category_input.currentIndex() == 0


def test_add_button_disabled_if_fields_empty(qtbot: QtBot, widget: AddExpenseWidget):
    add_button = widget.add_button
    date_input = widget.date_edit
    description_input = widget.description_edit
    category_input = widget.category_combo
    amount_input = widget.amount_edit

    assert not add_button.isEnabled()

    qtbot.keyClicks(date_input, "2022-03-10")
    assert not add_button.isEnabled()

    qtbot.keyClicks(description_input, "DragonBall")
    assert not add_button.isEnabled()

    category_input.setCurrentIndex(0)
    assert not add_button.isEnabled()

    qtbot.keyClicks(amount_input, "12.99")
    assert add_button.isEnabled()


# TODO: попробовать сделать так, чтобы во время тестов не выскакивали окна

def test_invalid_amount_warning_with_zero_value(qtbot):
    widget = AddExpenseWidget()
    qtbot.addWidget(widget)

    widget.date_edit.setText("2021-01-01")
    widget.description_edit.setText("Test expense")
    widget.category_combo.setCurrentIndex(0)
    widget.amount_edit.setText("0")
    message_box = widget._on_add_button_clicked()

    assert message_box is not None


def test_invalid_date_warning(qtbot):
    widget = AddExpenseWidget()
    qtbot.addWidget(widget)

    widget.date_edit.setText("2024-01-01")
    widget.description_edit.setText("Test expense")
    widget.category_combo.setCurrentIndex(0)
    widget.amount_edit.setText("10.00")
    message_box = widget._on_add_button_clicked()

    assert message_box is not None


def test_invalid_amount_warning_with_bad_format(qtbot):
    widget = AddExpenseWidget()
    qtbot.addWidget(widget)

    widget.date_edit.setText("2021-01-01")
    widget.description_edit.setText("Test expense")
    widget.category_combo.setCurrentIndex(0)
    widget.amount_edit.setText("sadasd")
    message_box = widget._on_add_button_clicked()

    assert message_box is not None

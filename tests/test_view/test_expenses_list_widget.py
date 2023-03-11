"""
Здесь содержатся тесты для виджета со списком расходов
"""
import pytest

from PyQt6 import QtCore

from bookkeeper.view.expenses_list_widget import ExpensesListWidget


@pytest.fixture
def expenses_list_widget(qtbot):
    widget = ExpensesListWidget()
    qtbot.addWidget(widget)
    return widget


def test_table(expenses_list_widget):
    """
    Проверяет верно ли, инициализируется таблица
    """
    assert expenses_list_widget.table.rowCount() == len(expenses_list_widget.expenses)
    assert expenses_list_widget.table.columnCount() == 5
    assert expenses_list_widget.table.horizontalHeaderItem(0).text() == "Дата"
    assert expenses_list_widget.table.horizontalHeaderItem(1).text() == "Название"
    assert expenses_list_widget.table.horizontalHeaderItem(2).text() == "Категория"
    assert expenses_list_widget.table.horizontalHeaderItem(3).text() == "Количество"
    assert expenses_list_widget.table.horizontalHeaderItem(4).text() == ""


def test_update_table(expenses_list_widget):
    """
    Проверяет верно ли, обновляется таблица
    """
    expenses_list_widget.expenses = [
        {"date": "2023-03-01", "description": "Продукты", "category": "Еда", "amount": "3000.00"},
        {"date": "2023-03-02", "description": "Питса", "category": "Еда", "amount": "700.00"},
    ]
    expenses_list_widget.update_table()
    assert expenses_list_widget.table.rowCount() == len(expenses_list_widget.expenses)
    assert expenses_list_widget.table.item(0, 0).text() == "2023-03-01"
    assert expenses_list_widget.table.item(0, 1).text() == "Продукты"
    assert expenses_list_widget.table.item(0, 2).text() == "Еда"
    assert expenses_list_widget.table.item(0, 3).text() == "3000.00"
    assert expenses_list_widget.table.cellWidget(0, 4) is not None


def test_delete_row(expenses_list_widget, qtbot):
    """
    Проверяет верно ли, удаляется строка
    """
    expenses_list_widget.expenses = [
        {"date": "2023-03-01", "description": "Продукты", "category": "Еда", "amount": "3000.00"},
        {"date": "2023-03-02", "description": "Питса", "category": "Еда", "amount": "700.00"},
    ]
    expenses_list_widget.expenses = [
        {"date": "2023-03-01", "description": "Продукты", "category": "Еда", "amount": "3000.00"},
        {"date": "2023-03-02", "description": "Питса", "category": "Еда", "amount": "700.00"},
    ]
    expenses_list_widget.update_table()
    delete_button = expenses_list_widget.table.cellWidget(0, 4)
    qtbot.mouseClick(delete_button, QtCore.Qt.MouseButton.LeftButton)
    assert expenses_list_widget.table.rowCount() == 1
    assert expenses_list_widget.expenses == [
        {"date": "2023-03-02", "description": "Питса", "category": "Еда", "amount": "700.00"}]


def test_add_row(expenses_list_widget):
    """
    Проверяет, что строка успешно добавляется
    """
    initial_row_count = expenses_list_widget.table.rowCount()
    expenses_list_widget.expenses.append(
        {"date": "2023-03-03", "description": "Кино", "category": "Развлечения", "amount": "500.00"}
    )
    expenses_list_widget.update_table()
    assert expenses_list_widget.table.rowCount() == initial_row_count + 1

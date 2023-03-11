"""
Здесь содержатся тесты для виджета со списком категорий
"""
import pytest

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout

from bookkeeper.view.category_widget import CategoryWidget


@pytest.fixture
def category_widget(qtbot):
    widget = CategoryWidget()
    qtbot.addWidget(widget)
    return widget


def test_initial_categories(category_widget):
    assert category_widget.list.count() == 5
    assert category_widget.list.item(0).text() == "Еда"
    assert category_widget.list.item(1).text() == "Транспорт"
    assert category_widget.list.item(2).text() == "Развлечения"
    assert category_widget.list.item(3).text() == "Дом"
    assert category_widget.list.item(4).text() == "Другое"


def test_add_duplicate_category(qtbot, category_widget):
    category_widget.name_edit.clear()

    category_widget.list.clear()
    category_widget.list.addItems(category_widget.categories)

    original_count = 0
    for i in range(category_widget.list.count()):
        item = category_widget.list.item(i)
        if item.text() == "Транспорт":
            original_count += 1

    category_widget.name_edit.setText("Транспорт")
    qtbot.mouseClick(category_widget.add_button, Qt.MouseButton.LeftButton)

    new_count = 0
    for i in range(category_widget.list.count()):
        item = category_widget.list.item(i)
        if item.text() == "Транспорт":
            new_count += 1

    assert category_widget.list.count() == 5
    assert new_count == original_count


def test_add_category(qtbot, category_widget):
    category_name = "Новая категория"
    category_widget.name_edit.setText(category_name)

    qtbot.mouseClick(category_widget.add_button, Qt.MouseButton.LeftButton)

    assert category_widget.list.count() == 6
    assert category_widget.list.item(5).text() == category_name


def test_delete_category(qtbot, category_widget):
    category_widget.list.setCurrentRow(2)

    qtbot.mouseClick(category_widget.delete_button, Qt.MouseButton.LeftButton)

    assert category_widget.list.count() == 4
    assert category_widget.list.item(2).text() != "Развлечения"


def test_edit_category(qtbot, category_widget):
    category_widget.list.setCurrentRow(1)
    category_widget.on_item_double_clicked(category_widget.list.currentItem())
    category_widget.list.currentItem().setText("Новое название категории")

    assert category_widget.list.count() == 5
    assert category_widget.list.item(1).text() == "Новое название категории"


def test_add_button_enabled(category_widget):
    category_widget.name_edit.clear()

    assert not category_widget.add_button.isEnabled()

    category_widget.name_edit.setText("Новая категория")

    assert category_widget.add_button.isEnabled()


def test_initial_name_edit(category_widget):
    assert category_widget.name_edit.text() == ""


def test_add_category_to_empty_list(qtbot, category_widget):
    category_widget.list.clear()

    category_name = "Новая категория"
    category_widget.name_edit.setText(category_name)

    qtbot.mouseClick(category_widget.add_button, Qt.MouseButton.LeftButton)

    assert category_widget.list.count() == 1
    assert category_widget.list.item(0).text() == category_name


def test_delete_category_from_empty_list(qtbot, category_widget):
    category_widget.list.clear()

    qtbot.mouseClick(category_widget.delete_button, Qt.MouseButton.LeftButton)

    assert category_widget.list.count() == 0


def test_edit_category_in_empty_list(qtbot, category_widget):
    category_widget.list.clear()

    category_widget.list.itemDoubleClicked.emit(None)
    assert category_widget.list.currentItem() is None


def test_add_category_with_special_characters(qtbot, category_widget):
    category_name = "!@#$%^&*"
    category_widget.name_edit.setText(category_name)

    qtbot.mouseClick(category_widget.add_button, Qt.MouseButton.LeftButton)

    assert category_widget.list.count() == 6
    assert category_widget.list.item(5).text() == category_name


def test_add_category_with_maximum_length_plus_one(qtbot, category_widget):
    max_length = 20

    category_name = "a" * (max_length + 1)
    category_widget.name_edit.setText(category_name)

    qtbot.mouseClick(category_widget.add_button, Qt.MouseButton.LeftButton)

    assert category_widget.list.count() == 6


def test_delete_all_categories(qtbot, category_widget):
    while category_widget.list.count() > 0:
        category_widget.list.setCurrentRow(0)

        qtbot.mouseClick(category_widget.delete_button, Qt.MouseButton.LeftButton)

    assert category_widget.list.count() == 0


def test_setup_ui(qtbot, category_widget):
    assert isinstance(category_widget.layout(), QVBoxLayout)
    assert isinstance(category_widget.layout().itemAt(0).widget(), QListWidget)
    assert isinstance(category_widget.layout().itemAt(1).layout(), QHBoxLayout)
    assert isinstance(category_widget.layout().itemAt(1).layout().itemAt(0).widget(), QPushButton)
    assert isinstance(category_widget.layout().itemAt(1).layout().itemAt(1).widget(), QPushButton)
    assert isinstance(category_widget.layout().itemAt(1).layout().itemAt(2).widget(), QLineEdit)

    assert not category_widget.add_button.isEnabled()


def test_on_editing_finished(qtbot, category_widget):
    category_name = "Новая категория"
    category_widget.name_edit.setText(category_name)
    qtbot.mouseClick(category_widget.add_button, Qt.MouseButton.LeftButton)

    category_widget.list.setCurrentRow(0)
    category_widget.on_item_double_clicked(category_widget.list.currentItem())
    category_widget.list.currentItem().setText("Измененная категория")

    qtbot.keyPress(category_widget.list, Qt.Key.Key_Return)

    assert category_widget.list.count() == 6
    assert category_widget.list.item(0).text() == "Измененная категория"


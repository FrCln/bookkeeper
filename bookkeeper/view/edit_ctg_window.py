"""
Widget of editing categories.
"""

from typing import Any, Callable
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QWidget, QTreeWidgetItem, QMenu, QMessageBox

from bookkeeper.view.presenters import CategoryPresenter
from bookkeeper.repository.repository_factory import RepositoryFactory
from bookkeeper.models.category import Category


class CategoryItem(QTreeWidgetItem):
    """Class represents QTreeWidgetItem with custom modifications.
    """
    def __init__(self, parent: Any, ctg: Category):
        super().__init__(parent, [ctg.name])
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)
        self.ctg = ctg

    def update(self, name: str) -> None:
        """Sets name of category.

        Args:
            name (str): name to set in category.
        """
        self.ctg.name = name

    def __str__(self) -> str:
        """Convertion to string.

        Returns:
            str: name of category.
        """
        return self.ctg.name


class EditCtgWindow(QWidget):
    """Class represents Widget of category editing.
    """
    ctg_changed = QtCore.Signal()

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Изменение категорий")

        layout = QtWidgets.QVBoxLayout()

        self.ctgs_widget = QtWidgets.QTreeWidget()
        self.ctgs_widget.setColumnCount(1)
        self.ctgs_widget.setHeaderLabel('Категории')

        layout.addWidget(self.ctgs_widget)
        self.setLayout(layout)
        self.presenter = CategoryPresenter(self, RepositoryFactory())

        self.menu = QMenu(self)
        self.menu.addAction('Добавить').triggered.connect(self.add_ctg_event)
        self.menu.addAction('Удалить').triggered.connect(self.delete_ctg_event)

        self.ctgs_widget.itemChanged.connect(self.edit_ctg_event)

    def get_selected_ctg(self) -> QTreeWidgetItem:
        """Returns selected QTreeWidgetItem.

        Returns:
            QTreeWidgetItem: selected Item
        """
        return self.ctgs_widget.currentItem()

    def register_ctg_adder(self, handler: Callable[[Category], None]) -> None:
        """Register of ctg_adder.
        """
        self.ctg_adder = handler

    def register_ctg_modifier(self, handler: Callable[[Category], None]) -> None:
        """Register of ctg_modifier.
        """
        self.ctg_modifier = handler

    def register_ctg_checker(self, handler: Callable[[str], bool]) -> None:
        """Register of ctg_checker.
        """
        self.ctg_checker = handler

    def register_ctg_deleter(self, handler: Callable[[Category], None]) -> None:
        """Register of ctg_deleter.
        """
        self.ctg_deleter = handler

    def register_ctg_finder(self, handler: Callable[[str], None | int]) -> None:
        """Register of ctg_finder.
        """
        self.ctg_finder = handler

    def set_ctg_list(self, ctgs: list[Category]) -> None:
        """Sets widget based on ctgs.

        Args:
            ctgs (list[Category]): Categories to set.
        """
        table = self.ctgs_widget
        uniq_pk: dict[int, CategoryItem] = {}

        set_once: bool = False
        for x in ctgs:
            pk = x.pk
            parent = x.parent

            # default parent is table.
            parent_ctg: Any = table
            if parent is not None:
                parent_ctg = uniq_pk.get(int(parent))

            ctg_item = CategoryItem(parent_ctg, x)
            uniq_pk.update({pk: ctg_item})
            if not set_once:
                table.setCurrentItem(ctg_item)
                set_once = True

    def contextMenuEvent(self, event: Any) -> None:
        """Mouse action.
        """
        self.menu.exec_(event.globalPos())

    def delete_ctg(self, ctg_item: CategoryItem, *_: int) -> None:
        """Deletes ctg_item from widget.

        Args:
            ctg_item (CategoryItem): Item to delete.
        """
        root = self.ctgs_widget.invisibleRootItem()
        (ctg_item.parent() or root).removeChild(ctg_item)

    def rename_ctg(self, ctg_item: CategoryItem, column: int) -> None:
        """Sets name of category.

        Args:
            ctg_item (CategoryItem): Item to get category from.
            column (int): column of item.
        """
        ctg_item.setText(column, ctg_item.ctg.name)

    def set_err_ctg(self, ctg_item: CategoryItem, column: int) -> None:
        """Sets error category.

        Args:
            ctg_item (CategoryItem): ctg to set error text.
        """
        ctg_item.setText(column, f'"{ctg_item.text(column)}"_err '
                         '(Wont be uploaded)')

    def edit_ctg_event(self, ctg_item: CategoryItem, column: int) -> None:
        """Event for processing category changes.

        Args:
            ctg_item (CategoryItem): Changed category
            column (int): column
        """
        entered_text = ctg_item.text(column)

        if ctg_item.ctg.pk == 0:
            action: Any = self.ctg_adder
            revert: Any = self.set_err_ctg
        else:
            action = self.ctg_modifier
            revert = self.rename_ctg

        if not self.ctg_checker(entered_text):
            self.ctgs_widget.itemChanged.disconnect()
            revert(ctg_item, column)
            self.ctgs_widget.itemChanged.connect(self.edit_ctg_event)
            QMessageBox.critical(self, 'Ошибка',
                                 f'Category {entered_text} already exists')
        else:
            ctg_item.update(entered_text)
            action(ctg_item.ctg)
            self.ctg_changed.emit()

    def add_ctg_event(self) -> None:
        """Event for processing Add action. Creates new category.
        """
        ctg_items = self.ctgs_widget.selectedItems()
        if len(ctg_items) == 0:
            parent_item: Any = self.ctgs_widget
            parent_pk = None
        else:
            assert len(ctg_items) == 1
            parent_item = ctg_items.pop()
            parent_pk = parent_item.ctg.pk

        if parent_pk == 0:
            QMessageBox.critical(self, 'Ошибка',
                                 'Создание подкатегории категории с ошибкой.')
            return

        self.ctgs_widget.itemChanged.disconnect()
        new_ctg = CategoryItem(parent_item, Category(parent=parent_pk))
        self.ctgs_widget.itemChanged.connect(self.edit_ctg_event)
        self.ctgs_widget.setCurrentItem(new_ctg)
        self.ctgs_widget.edit(self.ctgs_widget.currentIndex())

    def delete_ctg_event(self) -> None:
        """Event for processing Delete action. Deletes selected category.
        """
        ctg_item = self.ctgs_widget.currentItem()
        if ctg_item is None:
            return
        assert isinstance(ctg_item, CategoryItem)
        if ctg_item.ctg.pk == 0:
            self.delete_ctg(ctg_item)
            return

        confirm = QMessageBox.warning(self, 'Внимание',
                                      f'Вы уверены, что хотите удалить текущую "'
                                      f'{ctg_item.ctg.name}" и все дочерние категории?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if confirm == QMessageBox.No:
            return

        self.delete_ctg(ctg_item)
        self.ctg_deleter(ctg_item.ctg)
        self.ctg_changed.emit()

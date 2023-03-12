"""
Widget of expense table
"""

from datetime import datetime
from typing import Any, Callable

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QWidget, QTableWidget, QMenu, QMessageBox, QTableWidgetItem

from bookkeeper.view.edit_ctg_window import EditCtgWindow
from bookkeeper.view.presenters import ExpensePresenter
from bookkeeper.repository.repository_factory import RepositoryFactory
from bookkeeper.models.expense import Expense


class TableRow():
    """Class represents common feature inside one row.
    """
    def __init__(self, exp: Expense):
        self.exp = exp


class TableItem(QTableWidgetItem):
    """Class represents Item. Default - comment.
    """
    def __init__(self, row: TableRow):
        super().__init__()
        self.trow = row
        self.restore()

    def validate(self) -> bool:
        """Default Item is valid.

        Returns:
            bool: True
        """
        return True

    def restore(self) -> None:
        """Sets comment as text.
        """
        self.setText(self.trow.exp.comment)

    def update(self) -> None:
        """Sets text to comment.
        """
        self.trow.exp.comment = self.text()

    def get_err_msg(self) -> str:
        """Returns error message. Default - empty.

        Returns:
            str: Empty error string.
        """
        return ''

    def should_emit_on_upd(self) -> bool:
        """Indicates if changing of item should emit signal.

        Returns:
            bool: False.
        """
        return False


class TableAmountItem(TableItem):
    """Class represents Amount Item.
    """
    def validate(self) -> bool:
        """Vaildates if input is corrent.

        Returns:
            bool: True if input is correct, otherwise - False.
        """
        try:
            float(self.text())
        except ValueError:
            return False
        return True

    def restore(self) -> None:
        """Sets amount as text.
        """
        self.setText(str(round(self.trow.exp.amount, 2)))

    def update(self) -> None:
        """Sets amount from text.
        """
        self.trow.exp.amount = round(float(self.text()), 2)

    def get_err_msg(self) -> str:
        """Returns error message.
        """
        return 'Нужно ввести действительное число.'

    def should_emit_on_upd(self) -> bool:
        """When changing should emit signal.
        """
        return True


class TableCategoryItem(TableItem):
    """Class represents Category Item.
    """
    def __init__(self, row: TableRow, exp_view: Any):
        self.ctg_view = exp_view.ctg_view
        self.retriever = exp_view.ctg_retriever
        super().__init__(row)

    def validate(self) -> bool:
        """Vaildates if input is corrent.

        Returns:
            bool: True if input is correct, otherwise - False.
        """
        ctg_name = self.text()
        return not self.ctg_view.ctg_checker(ctg_name)

    def restore(self) -> None:
        """Sets category as text.
        """
        ctg = self.retriever(self.trow.exp.category)
        if ctg is None:
            # New ctg will have pk=0 and always drop here.
            ctg_item = self.ctg_view.get_selected_ctg()
            if ctg_item is None or ctg_item.ctg.pk == 0:
                raise ValueError('Категория не установлена')
            ctg = ctg_item.ctg.name
            self.trow.exp.category = ctg_item.ctg.pk
        self.setText(ctg)

    def update(self) -> None:
        """Sets category from text.
        """
        pk = self.ctg_view.ctg_finder(self.text())
        assert pk is not None
        self.trow.exp.category = pk

    def get_err_msg(self) -> str:
        """Returns error message.
        """
        return 'Нужно ввести существующую категорию.'


class TableDateItem(TableItem):
    """Class represents Date Item.
    """
    fmt = "%Y-%m-%d %H:%M:%S"

    def validate(self) -> bool:
        """Vaildates if input is corrent.

        Returns:
            bool: True if input is correct, otherwise - False.
        """
        date_str = self.text()
        try:
            datetime.fromisoformat(date_str)
        except ValueError:
            return False
        return True

    def restore(self) -> None:
        """Sets date as text.
        """
        date = self.trow.exp.expense_date
        self.setText(date.strftime(self.fmt))

    def get_err_msg(self) -> str:
        """Returns error message.
        """
        return f'Неверный формат даты.\nИспользуйте {self.fmt}'

    def update(self) -> None:
        """Sets date from text.
        """
        self.trow.exp.expense_date = datetime.fromisoformat(self.text())

    def should_emit_on_upd(self) -> bool:
        """When changing should emit signal.
        """
        return True


class Table(QTableWidget):
    """Class represents Table.
    """
    def __init__(self, parent: Any):
        super().__init__()
        self.wparent = parent
        self.setColumnCount(4)
        self.setRowCount(0)
        self.setHorizontalHeaderLabels("Дата "
                                       "Сумма "
                                       "Категория "
                                       "Комментарий".split())

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.verticalHeader().hide()

        self.menu = QMenu(self)
        self.menu.addAction('Добавить').triggered.connect(self.add_exp_event)
        self.menu.addAction('Удалить').triggered.connect(self.delete_exp_event)

        self.itemChanged.connect(self.update_exp_event)

    def update_exp_event(self, exp_item: TableItem) -> None:
        """Logic when item is changed.

        Args:
            exp_item (TableItem): Item to update.
        """
        if not exp_item.validate():
            self.itemChanged.disconnect()
            QMessageBox.critical(self, 'Ошибка', exp_item.get_err_msg())
            exp_item.restore()
            self.itemChanged.connect(self.update_exp_event)
            return

        exp_item.update()
        if isinstance(exp_item, TableAmountItem):
            self.itemChanged.disconnect()
            exp_item.restore()
            self.itemChanged.connect(self.update_exp_event)

        if exp_item.should_emit_on_upd():
            self.wparent.emit_exp_changed()

        self.wparent.exp_modifier(exp_item.trow.exp)

    def add_expense(self, exp: Expense) -> None:
        """Adds expense row.

        Args:
            exp (Expense): Expense to add.
        """
        row = TableRow(exp)
        ctg_item = TableCategoryItem(row, self.wparent)
        rcount = self.rowCount()
        self.setRowCount(rcount+1)
        self.itemChanged.disconnect()
        self.setItem(rcount, 0, TableDateItem(row))
        self.setItem(rcount, 1, TableAmountItem(row))
        self.setItem(rcount, 2, ctg_item)
        self.setItem(rcount, 3, TableItem(row))
        self.itemChanged.connect(self.update_exp_event)

    def delete_exp_event(self) -> None:
        """Deletes expense row.
        """
        row = self.currentRow()
        if row == -1:
            return
        confirm = QMessageBox.warning(self, 'Внимание',
                                      'Вы уверены, что хотите удалить текущую запись?"',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if confirm == QMessageBox.No:
            return
        titem = self.item(row, 0)
        self.removeRow(row)
        assert isinstance(titem, TableItem)
        exp_to_del = titem.trow.exp
        self.wparent.exp_deleter(exp_to_del)
        self.wparent.emit_exp_changed()

    def add_exp_event(self) -> None:
        """Logic on Add event.
        """
        exp = Expense()
        try:
            self.add_expense(exp)
        except ValueError as valerr:
            QMessageBox.critical(self, 'Ошибка', f'{valerr}')
            return
        self.wparent.exp_adder(exp)
        self.wparent.emit_exp_changed()

    def contextMenuEvent(self, event: Any) -> None:
        """Logic on Mouse event.
        """
        self.menu.exec_(event.globalPos())

    def update_ctgs(self) -> None:
        """Logic to update categories when they are chenged in CategoryWidget.
        """
        try:
            for row in range(self.rowCount()):
                titem = self.item(row, 2)
                assert isinstance(titem, TableItem)
                titem.restore()
        except ValueError as vallerr:
            QMessageBox.critical(self, 'Ошибка', f'Критическая ошибка.\n{vallerr}.\n'
                                 'Будут выставлены некоректные категории.')


class ExpenseWidget(QWidget):
    """Class represents Expense widget.
    """
    exp_changed = QtCore.Signal()

    def __init__(self, ctg_view: EditCtgWindow) -> None:
        super().__init__()
        self.ctg_view = ctg_view

        layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Последние расходы")
        layout.addWidget(message)

        self.table = Table(self)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.presenter = ExpensePresenter(self, RepositoryFactory())

    def register_ctg_retriever(self, handler: Callable[[int], None | str]) -> None:
        """Registers ctg_retriever.
        """
        self.ctg_retriever = handler

    def register_exp_adder(self, handler: Callable[[Expense], None]) -> None:
        """Registers exp_adder.
        """
        self.exp_adder = handler

    def register_exp_deleter(self, handler: Callable[[Expense], None]) -> None:
        """Registers exp_deleter.
        """
        self.exp_deleter = handler

    def register_exp_modifier(self, handler: Callable[[Expense], None]) -> None:
        """Registers exp_modifier.
        """
        self.exp_modifier = handler

    def set_exp_list(self, data: list[Expense]) -> None:
        """Sets expenses to table.

        Args:
            data (list[Expense]): Expenses to set.
        """
        list_to_delete: list[Expense] = []
        for x in data:
            try:
                self.table.add_expense(x)
            except ValueError as vallerr:
                QMessageBox.critical(self, 'Ошибка',
                                     f'Критическая ошибка.\n{vallerr}.\nЗапись '
                                     f'{x.expense_date.strftime("%Y-%m-%d %H:%M:%S")}'
                                     ' будет удалена.')
                list_to_delete.append(x)
        for x in list_to_delete:
            self.exp_deleter(x)

    def update_ctgs(self) -> None:
        """Updates categories.
        """
        self.table.update_ctgs()

    def emit_exp_changed(self) -> None:
        """Emit signal that expenses are changed.
        """
        self.exp_changed.emit()

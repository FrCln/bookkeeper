"""
Widget of expense table
"""

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import \
    (QWidget, QTableWidget, QMenu, QMessageBox, QTableWidgetItem)
from datetime import datetime

from .presenters import ExpensePresenter
from bookkeeper.repository.repository_factory import RepositoryFactory
from bookkeeper.models.expense import Expense
from .edit_ctg_window import EditCtgWindow


class TableRow:
    def __init__(self, exp: Expense):
        self.exp = exp


class TableItem(QTableWidgetItem):
    def __init__(self, row: TableRow):
        super().__init__()
        self.row = row
        self.restore()

    def validate(self) -> bool:
        return True

    def restore(self):
        self.setText(self.row.exp.comment)

    def update(self):
        self.row.exp.comment = self.text()

    def get_err_msg(self) -> str:
        pass

    def should_emit_on_upd(self) -> bool:
        return False


class TableAmountItem(TableItem):
    def __init__(self, row: TableRow):
        super().__init__(row)

    def validate(self) -> bool:
        try:
            float(self.text())
        except ValueError:
            return False
        return True

    def restore(self):
        self.setText(str(self.row.exp.amount))

    def update(self):
        self.row.exp.amount = float(self.text())

    def get_err_msg(self) -> str:
        return 'Нужно ввести действительное число.'

    def should_emit_on_upd(self) -> bool:
        return True


class TableCategoryItem(TableItem):
    def __init__(self, row: TableRow, exp_view):
        self.ctg_view = exp_view.ctg_view
        self.retriever = exp_view.ctg_retriever
        super().__init__(row)

    def validate(self) -> bool:
        ctg_name = self.text()
        return not self.ctg_view.ctg_checker(ctg_name)

    def restore(self):
        ctg = self.retriever(self.row.exp.category)
        if ctg is None:
            # New ctg will have pk=0 and always drop here.
            ctg_item = self.ctg_view.get_selected_ctg()
            if ctg_item is None:
                raise ValueError('Категория не установлена')
            ctg = ctg_item.ctg.name
            self.row.exp.category = ctg_item.ctg.pk
        self.setText(ctg)

    def update(self):
        pk = self.ctg_view.ctg_finder(self.text())
        assert pk is not None
        self.row.exp.category = pk

    def get_err_msg(self) -> str:
        return 'Нужно ввести существующую категорию.'


class TableDateItem(TableItem):
    fmt = "%Y-%m-%d %H:%M:%S"

    def __init__(self, row: TableRow):
        super().__init__(row)

    def validate(self) -> bool:
        date_str = self.text()
        try:
            datetime.fromisoformat(date_str)
        except ValueError:
            return False
        return True

    def restore(self):
        date = self.row.exp.expense_date
        self.setText(date.strftime(self.fmt))

    def get_err_msg(self) -> str:
        return f'Неверный формат даты.\nИспользуйте {self.fmt}'

    def update(self):
        self.row.exp.expense_date = datetime.fromisoformat(self.text())

    def should_emit_on_upd(self) -> bool:
        return True


class Table(QTableWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
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

    def update_exp_event(self, exp_item: TableItem):
        if not exp_item.validate():
            self.itemChanged.disconnect()
            QMessageBox.critical(self, 'Ошибка', exp_item.get_err_msg())
            exp_item.restore()
            self.itemChanged.connect(self.update_exp_event)
            return

        exp_item.update()

        if exp_item.should_emit_on_upd():
            self.parent.emit_exp_changed()

        self.parent.exp_modifier(exp_item.row.exp)

    def add_expense(self, exp: Expense):
        row = TableRow(exp)
        ctg_item = TableCategoryItem(row, self.parent)
        rc = self.rowCount()
        self.setRowCount(rc+1)
        self.itemChanged.disconnect()
        self.setItem(rc, 0, TableDateItem(row))
        self.setItem(rc, 1, TableAmountItem(row))
        self.setItem(rc, 2, ctg_item)
        self.setItem(rc, 3, TableItem(row))
        self.itemChanged.connect(self.update_exp_event)

    def delete_exp_event(self):
        row = self.currentRow()
        if row == -1:
            return
        confirm = QMessageBox.warning(self, 'Внимание',
                                      'Вы уверены, что хотите удалить текущую запись?"',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if confirm == QMessageBox.No:
            return
        self.removeRow(row)
        exp_to_del = self.item(row, 0).row.exp
        self.parent.exp_deleter(exp_to_del)
        self.parent.emit_exp_changed()

    def add_exp_event(self):
        exp = Expense()
        try:
            self.add_expense(exp)
        except ValueError as ve:
            QMessageBox.critical(self, 'Ошибка', f'{ve}')
            return
        self.parent.exp_adder(exp)
        self.parent.emit_exp_changed()

    def contextMenuEvent(self, event):
        self.menu.exec_(event.globalPos())

    def update_ctgs(self):
        try:
            for row in range(self.rowCount()):
                self.item(row, 2).restore()
        except ValueError as ve:
            QMessageBox.critical(self, 'Ошибка',
                                 f'Критическая ошибка.\n{ve}.'
                                 f'\nБудут выставлены некорректные категории.')


class ExpenseWidget(QWidget):
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

    def register_ctg_retriever(self, handler):
        self.ctg_retriever = handler

    def register_exp_adder(self, handler):
        self.exp_adder = handler

    def register_exp_deleter(self, handler):
        self.exp_deleter = handler

    def register_exp_modifier(self, handler):
        self.exp_modifier = handler

    def set_exp_list(self, data: list[Expense]):
        list_to_delete: list[Expense] = []
        for x in data:
            try:
                self.table.add_expense(x)
            except ValueError as ve:
                QMessageBox.critical(self, 'Ошибка',
                                     f'Критическая ошибка.\n{ve}.'
                                     f'\n'f'Запись '
                                     f'{x.expense_date.strftime("%Y-%m-%d %H:%M:%S")} '
                                     f'будет удалена.')
                list_to_delete.append(x)
        for x in list_to_delete:
            self.exp_deleter(x)

    def update_ctgs(self):
        self.table.update_ctgs()

    def emit_exp_changed(self):
        self.exp_changed.emit()

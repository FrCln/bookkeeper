from datetime import datetime
from typing import List

from PyQt6.QtWidgets import QMessageBox

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.view import main_window
from bookkeeper.view.expenses_list_widget import ExpensesListWidget
from bookkeeper.view.category_widget import CategoryWidget
from bookkeeper.view.add_expense_widget import AddExpenseWidget
from bookkeeper.view.budget_widget import BudgetWidget
from bookkeeper.view.main_window import MainWindow


class Presenter:
    """
    Presenter Bookkeeper, связывает MODEL и VIEW.
    """

    def __init__(self, exp_repo: AbstractRepository[Expense],
                 cat_repo: AbstractRepository[Category]) -> None:
        self.cat_repo = cat_repo
        self.exp_repo = exp_repo

    def show_main_window(self):
        self.main_window = MainWindow()

        # инициализирует таблицу расходов
        self.init_table()

        # инициализирует список категорий
        self.init_category()

        # соединяем сигналы
        self.main_window.expenses_list_widget.delete_button_clicked.connect(self.delete_expense)
        self.main_window.add_expense_widget.expense_added.connect(self.add_expense)
        self.main_window.expenses_list_widget.category_cell_double_clicked.connect(
            self._on_category_cell_double_clicked)
        self.main_window.expenses_list_widget.category_cell_changed.connect(self._on_category_cell_changed)
        self.main_window.expenses_list_widget.expense_cell_changed.connect(self.update_expense)

        # обновление таблицы расходов и категорий
        self.update_expenses_list()
        self.update_category_list()

        self.main_window.show()

    def init_table(self) -> None:
        self.main_window.expenses_list_widget.init_table()

    def init_category(self) -> None:
        categories = [category.name for category in self.cat_repo.get_all()]
        self.main_window.category_widget.list.clear()
        self.main_window.category_widget.init_category_list(categories)

    def update_expenses_list(self) -> None:
        """
        Обновляет содержимое таблицы расходов
        на основе данных из репозитория.
        """

        objects = self.exp_repo.get_all()
        expenses = [expense for expense in objects if isinstance(expense, Expense)]
        expenses_dict = []
        # сопоставляем объекты Expense со словарём в виджете
        for expense in expenses:
            category = self.cat_repo.get(expense.category)
            expense_dict = {
                "date": datetime.strptime(expense.expense_date, "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d"),
                "description": expense.comment,
                "category": str(category.name),
                "amount": str(expense.amount)
            }
            expenses_dict.append(expense_dict)
        self.main_window.expenses_list_widget.update_table(expenses_dict)

    def delete_expense(self, index: int) -> None:
        """
        Удаляет расход из базы данных и обновляет содержимое таблицы.
        """
        try:
            objects = self.exp_repo.get_all()
            expenses = [expense for expense in objects if isinstance(expense, Expense)]
            expense = expenses[index]
            self.exp_repo.delete(expense.pk)
            self.update_expenses_list()
        except Exception as e:
            print(f"Ошибка delete_expense: {e}")

    def update_category_list(self) -> None:
        """
        Обновляет содержимое списка категорий в комбобоксе виджета добавления расхода
        на основе данных из репозитория.
        """
        categories = self.cat_repo.get_all()
        categories_list = [(category.pk, category.name) for category in categories]
        self.main_window.add_expense_widget.set_categories(categories_list)

    def _on_category_cell_double_clicked(self, row: int, column: int, category_name: str) -> None:
        categories = self.cat_repo.get_all()
        categories = [(category.pk, category.name) for category in categories]
        self.main_window.expenses_list_widget._update_category_cell(row, column, categories)

    def _on_category_cell_changed(self, row: int, column: int, category_id: int) -> None:
        expense_id = self.exp_repo.get_all()[row].pk
        expense = self.exp_repo.get(expense_id)
        category = self.cat_repo.get(category_id)

        try:
            print("_on_category_cell_changed запущен")
            msg_box = QMessageBox()
            msg_box.setText(f"Вы действительно хотите изменить категорию на {category.name}?")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg_box.setDefaultButton(QMessageBox.StandardButton.No)
            yes_button = msg_box.button(QMessageBox.StandardButton.Yes)
            yes_button.setText("Да")
            no_button = msg_box.button(QMessageBox.StandardButton.No)
            no_button.setText("Нет")
            ret = msg_box.exec()
            if ret == QMessageBox.StandardButton.Yes:
                expense.category = category_id
                self.exp_repo.update(expense)
                self.update_expenses_list()
            else:
                self.update_expenses_list()

        except Exception as e:
            print(f"Ошибка _on_category_cell_changed: {e}")

    def add_expense(self) -> None:
        """
        Создает новый объект Expense на основе данных из виджета
        AddExpenseWidget и добавляет его в репозиторий. Обновляет
        содержимое таблицы расходов.
        """
        comment = self.main_window.add_expense_widget.description_edit.text()
        # для поиска pk категории на основе названия:
        category_name = self.main_window.add_expense_widget.category_combo.currentText()
        category_id = next((id for id, name in self.main_window.add_expense_widget.categories if name == category_name),
                           None)
        amount = self.main_window.add_expense_widget.amount_edit.text()

        expense = Expense(amount, category_id, datetime.now(), datetime.now(), comment)
        try:
            self.exp_repo.add(expense)
            self.update_expenses_list()
        except Exception as e:
            print(f"Ошибка add_expense: {e}")

    def update_expense(self, row: int, column: int, new_value: str) -> None:
        objects = self.exp_repo.get_all()
        expenses = [expense for expense in objects if isinstance(expense, Expense)]
        expense = expenses[row]
        if column == 1:
            expense.amount = int(new_value)
        elif column == 2:
            expense.expense_date = datetime.strptime(new_value, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S.%f')
        elif column == 3:
            expense.comment = new_value
        try:
            self.exp_repo.update(expense)
            self.update_expenses_list()
        except Exception as e:
            print(f"Ошибка update_expense: {e}")


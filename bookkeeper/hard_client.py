"""
Тестовый скрипт для графического приложения
"""
# mypy: disable-error-code="index,type-arg"
from datetime import datetime

from bookkeeper.view.view import View
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.abstract_repository import AbstractRepository as Repo
from bookkeeper.utils import read_tree


class BookkeeperClient:
    """
    Класс, описывающий представление (Presenter)
    """
    def __init__(self, main_view: View, repo_type: type):
        self.view = main_view

        self.cat_repo: Repo = repo_type[Category]("../dbfiles/database.db", Category)
        self.exp_repo: Repo = repo_type[Expense]("../dbfiles/database.db", Expense)
        self.budget_repo: Repo = repo_type[Budget]("../dbfiles/database.db", Budget)

        self.view.set_categories(self.cat_repo.get_all())
        self.view.set_expenses(self.exp_repo.get_all())
        self.view.set_budget(self.budget_repo.get_all())

        self.view.set_cat_edit_open_callback(self.cat_edit_open_callback)
        self.view.set_exp_add_callback(self.exp_add_callback)
        self.view.set_cat_edit_save_callback(self.cat_edit_save_callback)
        self.view.set_exp_table_changed_callback(self.exp_table_changed_callback)
        self.view.set_budget_table_changed_callback(self.budget_table_changed_callback)

    def run(self) -> None:
        """
        Запускает отображение представления
        """
        self.view.run()

    def cat_edit_open_callback(self) -> None:
        """
        Обработка события: открыть окно редактирования категорий
        """
        self.view.show_category_edit_window()
        self.view.set_cat_text(Category.get_all_as_tree(self.cat_repo))

    def exp_add_callback(self, amount: str, category_name: str) -> None:
        """
        Обработка события: добавить расход
        """
        cat = self.cat_repo.get_all({'name': category_name})[0]
        exp = Expense(int(amount), cat.pk)
        self.exp_repo.add(exp)

        self.view.set_expenses(self.exp_repo.get_all())

        budgets: list[Budget] = self.budget_repo.get_all()

        for i in budgets:
            i.update_with_expenses(self.exp_repo)
            self.budget_repo.update(i)

        self.view.set_budget(self.budget_repo.get_all())

    def cat_edit_save_callback(self, text: str) -> None:
        """
        Обработка события: сохранить новые категории
        """
        try:
            local_repo = MemoryRepository[Category]()
            Category.create_from_tree(read_tree(text.splitlines()), local_repo)

            self.cat_repo.clear()
            Category.create_from_tree(read_tree(text.splitlines()), self.cat_repo)
            self.view.set_categories(self.cat_repo.get_all())

        except IndentationError:
            print("Error while converting categories")

    def exp_table_changed_callback(self, pk: int, attr: str, value: str) -> None:
        """
        Обработка события: изменение данных в таблице расходов
        """
        obj = self.exp_repo.get(pk)
        match attr:
            case "amount":
                setattr(obj, attr, int(value))
            case "category":
                setattr(obj, attr, self.cat_repo.get_all({'name': value})[0].pk)
            case "expense_date":
                setattr(obj, attr, datetime.strptime(value, "%d.%m.%Y %H:%M"))
            case "added_date":
                setattr(obj, attr, datetime.strptime(value, "%d.%m.%Y %H:%M"))
            case "comment":
                setattr(obj, attr, value)

        self.exp_repo.update(obj)

    def budget_table_changed_callback(self, period: str, attr: str, value: str) -> None:
        """
        Обработка события: изменение данных в таблице бюджета
        """
        obj = self.budget_repo.get_all({'period': period})[0]
        setattr(obj, attr, int(value))

        self.budget_repo.update(obj)


if __name__ == "__main__":
    view = View()
    client = BookkeeperClient(view, SQLiteRepository)
    client.run()

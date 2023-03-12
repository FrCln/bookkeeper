"""Module contains MVPs to isolate view and db logics.
"""

from typing import Protocol, Callable
from datetime import datetime, timedelta

from bookkeeper.repository.repository_factory import AbsRepoFactory
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense


class AbstractExpenseView(Protocol):
    """Protocol for ExpenseView.
    """
    def register_exp_adder(self, handler: Callable[[Expense], None]) -> None:
        """Registers view's exp_adder.
        """

    def register_exp_deleter(self, handler: Callable[[Expense], None]) -> None:
        """Registers view's exp_deleter.
        """

    def register_exp_modifier(self, handler: Callable[[Expense], None]) -> None:
        """Registers view's exp_modifier.
        """

    def register_ctg_retriever(self, handler: Callable[[int], str | None]) -> None:
        """Registers view's exp_retriever.
        """

    def set_exp_list(self, data: list[Expense]) -> None:
        """Sets expenses.
        """


class AbstractCategoryView(Protocol):
    """Protocol for CatogoryView.
    """
    def set_ctg_list(self, ctgs: list[Category]) -> None:
        """Sets categories.
        """

    def register_ctg_modifier(self, handler: Callable[[Category], None]) -> None:
        """Registers view's ctg_modifier.
        """

    def register_ctg_adder(self, handler: Callable[[Category], None]) -> None:
        """Registers view's ctg_adder.
        """

    def register_ctg_checker(self, handler: Callable[[str], bool]) -> None:
        """Registers view's ctg_checker.
        """

    def register_ctg_finder(self, handler: Callable[[str], None | int]) -> None:
        """Registers view's ctg_finder.
        """

    def register_ctg_deleter(self, handler: Callable[[Category], None]) -> None:
        """Registers view's ctg_deleter.
        """


class CategoryPresenter:
    """Class represents presenter for Category model.
    """
    def __init__(self,  view: AbstractCategoryView, repository_factory: AbsRepoFactory):
        self.view = view
        self.ctg_repo = repository_factory.get(Category)

        self.ctgs = self.ctg_repo.get_all()
        self.view.set_ctg_list(self.ctgs)
        self.view.register_ctg_modifier(self.modify_ctg)
        self.view.register_ctg_adder(self.add_ctg)
        self.view.register_ctg_checker(self.check_name)
        self.view.register_ctg_deleter(self.delete_ctg)
        self.view.register_ctg_finder(self.find_ctg_by_name)

    def modify_ctg(self, ctg: Category) -> None:
        """Updates category in repo.

        Args:
            ctg (Category): category to update.
        """
        self.ctg_repo.update(ctg)

    def check_name(self, name: str) -> bool:
        """Checks is name in category list.

        Args:
            name (str): name to check.

        Returns:
            bool: True if there is no such name, otherwise - False.
        """
        if name in [c.name for c in self.ctgs]:
            return False
        return True

    def find_ctg_by_name(self, name: str) -> int | None:
        """Returns pk of category with name.

        Args:
            name (str): name to find.

        Returns:
            int | None: Returns pk of found category. None if category is not found.
        """
        for x in self.ctgs:
            if x.name == name:
                return x.pk
        return None

    def add_ctg(self, ctg: Category) -> None:
        """Creates new category in DB.

        Args:
            ctg (Category): Category to add.
        """
        self.ctg_repo.add(ctg)
        self.ctgs.append(ctg)

    def delete_ctg(self, top_lvl_ctg: Category) -> None:
        """Deletes category and all children from DB.

        Args:
            top_lvl_ctg (Category): root category to delete.
        """
        queue = [top_lvl_ctg]
        to_delete = []

        while len(queue) != 0:
            proc = queue.pop()
            to_delete.append(proc)
            queue.extend([x for x in self.ctgs if x.parent == proc.pk])

        for x in to_delete:
            self.ctgs.remove(x)
            self.ctg_repo.delete(x.pk)


class ExpensePresenter:
    """Class represents presenter for Expense model.
    """
    def __init__(self,  view: AbstractExpenseView, repository_factory: AbsRepoFactory):
        self.view = view
        self.repo = repository_factory.get(Expense)
        self.ctg_repo = repository_factory.get(Category)

        self.exps = self.repo.get_all()
        self.view.register_exp_adder(self.add_exp)
        self.view.register_exp_deleter(self.delete_exp)
        self.view.register_exp_modifier(self.modify_exp)
        self.view.register_ctg_retriever(self.retrieve_ctg)
        self.view.set_exp_list(self.exps)

    def retrieve_ctg(self, pk: int) -> str | None:
        """Gets category name with pk.

        Args:
            pk (int): pk to find.

        Returns:
            str | None: Found category name or None if is not found.
        """
        ctg = self.ctg_repo.get(pk)
        if ctg is None:
            return None
        return ctg.name

    def add_exp(self, exp: Expense) -> None:
        """Creates new expense record in db.

        Args:
            exp (Expense): expense to create.
        """
        self.repo.add(exp)
        self.exps.append(exp)

    def delete_exp(self, exp: Expense) -> None:
        """Deletes expense record from db.

        Args:
            exp (Expense): expense to delete.
        """
        self.exps.remove(exp)
        self.repo.delete(exp.pk)

    def modify_exp(self, exp: Expense) -> None:
        """Updates expense record in db.

        Args:
            exp (Expense): expense to update.
        """
        self.repo.update(exp)

    def get_expenses_from_till(self, start: datetime, end: datetime) -> list[float]:
        """Gets all expense amounts from start date till end date.

        Args:
            start (datetime): begin date
            end (datetime): end date

        Returns:
            list[float]: expense amounts.
        """
        assert start > end
        exps = [x.amount for x in self.exps
                if x.expense_date < start and x.expense_date > end]
        return exps


class AbstractBudgetView(Protocol):
    """Protocol for BudgetView.
    """
    exp_presenter: ExpensePresenter

    def register_bgt_modifier(self, handler: Callable[[Budget], None]) -> None:
        """Registers view's bgt_modifier.
        """

    def register_bgt_getter(self, handler: Callable[[], Budget]) -> None:
        """Registers view's bgt_getter.
        """

    def register_exp_getter(self, handler: Callable[[], list[float]]) -> None:
        """Registers view's exp_getter.
        """


class BudgetPresenter:
    """Class represents presenter for Budget model.
    """
    def __init__(self,  view: AbstractBudgetView, repository_factory: AbsRepoFactory):
        self.view = view
        self.exp_presenter = self.view.exp_presenter
        self.repo = repository_factory.get(Budget)
        self.view.register_bgt_modifier(self.modify_bgt)
        self.view.register_bgt_getter(self.get_bgt)
        self.view.register_exp_getter(self.get_exp)

    def get_exp(self) -> list[float]:
        """Returns list of expenses for day, week and month.

        Returns:
            list[float]: expenses.
        """
        now = datetime.now()
        day = now - timedelta(days=1)
        week = now - timedelta(weeks=1)
        month = now - timedelta(days=30)

        exp_day = sum(self.exp_presenter.get_expenses_from_till(now, day))
        exp_week = sum(self.exp_presenter.get_expenses_from_till(now, week))
        exp_month = sum(self.exp_presenter.get_expenses_from_till(now, month))
        return [exp_day, exp_week, exp_month]

    def modify_bgt(self, bgt: Budget) -> None:
        """Updates budget in db.

        Args:
            bgt (Budget): budget to update.
        """
        self.repo.update(bgt)

    def get_bgt(self) -> Budget:
        """Gets budget from db.
        If there is no any budget - creates default.

        Returns:
            Budget: budget from db.
        """
        bgts = self.repo.get_all()
        if len(bgts) == 0:
            bgt = Budget(0)
            self.repo.add(bgt)
            bgts.append(bgt)

        assert len(bgts) == 1
        return bgts.pop()

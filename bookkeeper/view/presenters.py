
from typing import Protocol
from datetime import datetime, timedelta

from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense


class AbstractView(Protocol):
    def set_ctg_list(notused: list[Category]) -> None:
        pass

    def register_ctg_modifier(handler):
        pass

    def register_ctg_adder(handler):
        pass

    def register_ctg_checker(handler):
        pass

    def register_ctg_finder(handler):
        pass

    def register_ctg_deleter(handler):
        pass

    def register_bgt_modifier(handler):
        pass

    def register_bgt_getter(handler):
        pass

    def register_ctg_retriever(handler):
        pass

    def register_exp_getter(handler):
        pass


class CategoryPresenter:
    def __init__(self,  view: AbstractView, repository_factory):
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
        self.ctg_repo.update(ctg)

    def check_name(self, name: str) -> bool:
        if name in [c.name for c in self.ctgs]:
            return False
        return True

    def find_ctg_by_name(self, name: str) -> int | None:
        for x in self.ctgs:
            if x.name == name:
                return x.pk
        return None

    def add_ctg(self, ctg: Category) -> None:
        self.ctg_repo.add(ctg)
        self.ctgs.append(ctg)

    def delete_ctg(self, top_lvl_ctg: Category) -> None:
        queue = [top_lvl_ctg]
        to_delete = list()

        while len(queue) != 0:
            proc = queue.pop()
            to_delete.append(proc)
            queue.extend([x for x in self.ctgs if x.parent == proc.pk])

        for x in to_delete:
            self.ctgs.remove(x)
            self.ctg_repo.delete(x.pk)


class BudgetPresenter:
    def __init__(self,  view: AbstractView, repository_factory):
        self.view = view
        self.exp_presenter = self.view.exp_presenter
        self.repo = repository_factory.get(Budget)
        self.view.register_bgt_modifier(self.modify_bgt)
        self.view.register_bgt_getter(self.get_bgt)
        self.view.register_exp_getter(self.get_exp)

    def get_exp(self) -> list[float]:
        now = datetime.now()
        day = now - timedelta(days=1)
        week = now - timedelta(weeks=1)
        month = now - timedelta(days=30)

        exp_day = sum(self.exp_presenter.get_expenses_from_till(now, day))
        exp_week = sum(self.exp_presenter.get_expenses_from_till(now, week))
        exp_month = sum(self.exp_presenter.get_expenses_from_till(now, month))
        return [exp_day, exp_week, exp_month]

    def modify_bgt(self, bgt: Budget):
        self.repo.update(bgt)

    def get_bgt(self) -> Budget:
        bgts = self.repo.get_all()
        if len(bgts) == 0:
            bgt = Budget(0)
            self.repo.add(bgt)
            bgts.append(bgt)

        assert len(bgts) == 1
        return bgts.pop()


class ExpensePresenter:
    def __init__(self,  view: AbstractView, repository_factory):
        self.view = view
        self.repo = repository_factory.get(Expense)
        self.ctg_repo = repository_factory.get(Category)

        self.exps = self.repo.get_all()
        self.view.register_exp_adder(self.add_exp)
        self.view.register_exp_deleter(self.delete_exp)
        self.view.register_exp_modifier(self.modify_exp)
        self.view.register_ctg_retriever(self.retrieve_ctg)
        self.view.set_exp_list(self.exps)

    def retrieve_ctg(self, pk: int) -> str:
        ctg = self.ctg_repo.get(pk)
        if ctg is None:
            return None
        return ctg.name

    def add_exp(self, exp: Expense):
        self.repo.add(exp)
        self.exps.append(exp)

    def delete_exp(self, exp: Expense):
        self.exps.remove(exp)
        self.repo.delete(exp.pk)

    def modify_exp(self, exp: Expense):
        self.repo.update(exp)

    def get_expenses_from_till(self, start: datetime, end: datetime) -> list[float]:
        assert start > end
        exps = [x.amount for x in self.exps
                if x.expense_date < start and x.expense_date > end]
        return exps

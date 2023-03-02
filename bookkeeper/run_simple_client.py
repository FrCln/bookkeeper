"""
Логика для скриптов simple_client
"""
from typing import Optional

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.utils import read_tree
from bookkeeper.repository.abstract_repository import AbstractRepository


def create_categories(cat_repo: AbstractRepository[Category]) -> None:
    """
    Функция для создания категорий
    """
    cats = '''
    продукты
        мясо
            сырое мясо
            мясные продукты
        сладости
    книги
    одежда
    '''.splitlines()
    Category.create_from_tree(read_tree(cats), cat_repo)


def create_budget(bud_repo: AbstractRepository[Budget]) -> Optional[Budget]:
    """
    Функция для создания бюджета
    """
    crt_budget = input('Хотите ли вы создать бюджет на этот месяц? (y/n): ')
    if crt_budget.lower() == 'y':
        budget_amount = float(input('Введите месячный бюджет: '))
        budget = Budget.create_for_current_month(budget_amount, bud_repo)
        return budget
    return None


def handle_user_input(cmd: str, cat_repo: AbstractRepository[Category],
                      exp_repo: AbstractRepository[Expense],
                      budget: Optional[Budget], bud_repo: AbstractRepository[Budget]) \
        -> Optional[Budget]:
    """
    Обрабатывает команды пользовательского ввода и обновляет данные
    """
    if cmd == 'категории':
        print(*cat_repo.get_all(), sep='\n')
    elif cmd == 'расходы':
        print(*exp_repo.get_all(), sep='\n')
    elif cmd == 'бюджеты':
        print(*bud_repo.get_all(), sep='\n')
    elif cmd[0].isdecimal():
        amount, name = cmd.split(maxsplit=1)
        try:
            cat = cat_repo.get_all({'name': name})[0]
        except IndexError:
            print(f'категория {name} не найдена')
            return budget
        exp = Expense(int(amount), cat.pk)
        if budget is not None and exp.amount > budget.amount:
            if budget.amount == 0:
                print('Бюджет на этот месяц исчерпан')
            else:
                print(f'Сумма расхода ({exp.amount}) '
                      f'превышает бюджет ({budget.amount})')
                return budget
        exp_repo.add(exp)
        if budget is not None:
            budget.amount -= exp.amount
            bud_repo.update(budget)
            print(f'Остаток бюджета: {budget.amount}')
        print(exp)
    return budget


def run_simple_client(cat_repo: AbstractRepository[Category],
                      exp_repo: AbstractRepository[Expense],
                      bud_repo: AbstractRepository[Budget]) -> None:
    """
    Функция для запуска категорий
    """
    create_categories(cat_repo)
    budget = create_budget(bud_repo)

    while True:
        try:
            cmd = input('$> ')
        except EOFError:
            break
        if not cmd:
            continue
        budget = handle_user_input(cmd, cat_repo, exp_repo, budget, bud_repo)

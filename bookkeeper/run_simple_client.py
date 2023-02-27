"""
Функция для запуска sql_simple_client и simple_client
Также содержит в себе категории
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.utils import read_tree
from bookkeeper.repository.abstract_repository import AbstractRepository


def run_simple_client(cat_repo: AbstractRepository[Category],
                      exp_repo: AbstractRepository[Expense]) \
        -> None:

    """
    cats содержит в себе категории
    далее описана логика работы терминала
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

    while True:
        try:
            cmd = input('$> ')
        except EOFError:
            break
        if not cmd:
            continue
        if cmd == 'категории':
            print(*cat_repo.get_all(), sep='\n')
        elif cmd == 'расходы':
            print(*exp_repo.get_all(), sep='\n')
        elif cmd[0].isdecimal():
            amount, name = cmd.split(maxsplit=1)
            try:
                cat = cat_repo.get_all({'name': name})[0]
            except IndexError:
                print(f'категория {name} не найдена')
                continue
            exp = Expense(int(amount), cat.pk)
            exp_repo.add(exp)
            print(exp)

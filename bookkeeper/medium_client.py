"""
Тестовый скрипт для терминала средней сложности
"""
# pylint: disable=duplicate-code
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree

cat_repo = SQLiteRepository[Category]("../dbfiles/database.db", Category)
exp_repo = SQLiteRepository[Expense]("../dbfiles/database.db", Expense)
budget_repo = SQLiteRepository[Budget]("../dbfiles/database.db", Budget)

if len(cat_repo.get_all()) == 0:

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

if (len(budget_repo.get_all())) == 0:
    b1 = Budget(total=1000, period="day")
    b1.update_with_expenses(exp_repo)
    budget_repo.add(b1)

    b2 = Budget(total=30000, period="week")
    b2.update_with_expenses(exp_repo)
    budget_repo.add(b2)

    b3 = Budget(total=30000*12, period="month")
    b3.update_with_expenses(exp_repo)
    budget_repo.add(b3)

while True:  # noqa: C901
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
    elif cmd == 'бюджет':
        print(*budget_repo.get_all(), sep='\n')
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

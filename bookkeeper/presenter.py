import sys 

from bookkeeper.view.Redactclass import MyMainWindow, RedactField, CatChoice, MainTable
from bookkeeper.view.redactmenu import RedactMenu,CommentMenu
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository, ExpenseRepository
from bookkeeper.utils import read_tree
from datetime import datetime
from PySide6 import QtWidgets, QtCore, QtGui

cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()


expense_test = Expense(2, 4, datetime(2020, 5 ,17), comment = "Bought some bread")
expense_test1 = Expense(100, 3, datetime(2013, 9, 17), comment = "gta 5")

cat_repo = SQLiteRepository[Category]('categories.db', Category)
exp_repo = ExpenseRepository('expences.db', Expense)
exp_repo.add(expense_test)
exp_repo.add(expense_test1)
Category.create_from_tree(read_tree(cats), cat_repo)

class CategoryPresenter:
    def __init__(self, window, cat_repo):
        self.window = window
        self.category_db = cat_repo
        self.cats = self.category_db.get_all()
        self.cat_list = []
        for cat in self.cats:
            self.cat_list.append(cat.name)
            
        self.window.set_categories(self.cat_list)
       
class ExpencePresenter:
    def __init__(self, window, exp_repo, cat_repo):
        self.window = window
        self.expense_db = exp_repo
        self.expenses = self.expense_db.get_all()
        self.data_to_fill = []
        self.sum = 0
        for exp in self.expenses:
            attrs = []
            attrs.append(exp.added_date)
            attrs.append(str(exp.amount))
            exp_cat = cat_repo.get(exp.category).name 
            attrs.append(exp_cat)
            attrs.append(exp.expense_date)
            attrs.append(exp.comment)
            self.data_to_fill.append(attrs)
        for datas in self.data_to_fill:
            self.sum += int(datas[1])
            
        self.window.fill_table_data(self.data_to_fill)
        self.window.add_given_amount(str(self.sum))
        

app = QtWidgets.QApplication(sys.argv)
window = MyMainWindow()
wind_ruler = CategoryPresenter(window, cat_repo)
exp_manage = ExpencePresenter(window, exp_repo, cat_repo)
window.show()
sys.exit(app.exec())


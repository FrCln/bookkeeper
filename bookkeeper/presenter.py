import sys 

from bookkeeper.view.Redactclass import MyMainWindow, RedactField, CatChoice, MainTable
from bookkeeper.view.redactmenu import RedactMenu,CommentMenu
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree
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


expense_test = Expense(2, "продукты", "13.05.2020", "12.06.2020", "Bought some bread", 3)

cat_repo = SQLiteRepository[Category]('categories.db', Category)
#exp_repo = SQLiteRepository[Expense]('expences.db', Expense)
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
       
#class ExpencePresenter:
#    def __init__(self, window, exp_repo):
        

app = QtWidgets.QApplication(sys.argv)
window = MyMainWindow()
wind_ruler = CategoryPresenter(window, cat_repo)
window.show()
sys.exit(app.exec())


import sys
from bookkeeper.view.Redactclass import MyMainWindow
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository, ExpenseRepository
from bookkeeper.utils import read_tree
from datetime import datetime
from PySide6 import QtWidgets

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
"""Добавляем два расхода в таблицу расходов"""
exp_repo.add(expense_test)
exp_repo.add(expense_test1)
"""Заполняем таблицу категорий значениями из cats"""
categories_list = Category.create_from_tree(read_tree(cats), cat_repo)

class CategoryPresenter:
    """Класс, отвечающий за связь базы данных с категориями 
    с списком категорий в виджете"""
    def __init__(self, window, cat_repo):
        self.window = window
        self.category_db = cat_repo
        self.cats = self.category_db.get_all()
        self.cat_names= []
        for cat in self.cats:
            self.cat_names.append(cat.name)
        self.window.set_categories(self.cat_names)
        self.window.register_cat_adder(self.add_cat)
        self.window.register_cat_deleter(self.delete_cat)
    
    def add_cat(self, cat, parent):
        """Добавление категорий в таблицу по сигналу 
        из виджета"""
        if parent in self.cat_names:
            parent_id = self.cat_names.index(parent) + 1
            self.category_db.add(Category(name = cat, parent = parent_id))
        else:
            self.category_db.add(Category(name = cat))
        self.cat_names.append(cat)
        self.cats.append(self.category_db.get(len(self.cat_names)))
    
    def delete_cat(self, cat):
        """Удаление категории из таблицы
        по команде с виджета"""
        cat_id = self.cat_names.index(cat)
        for categ in self.cats:
            print(categ)
            if categ.parent == cat_id + 1:
                categ.parent = None
                self.category_db.update(categ)
        self.category_db.delete(cat_id + 1)
        self.cat_names.pop(cat_id)
        self.cats.pop(cat_id)

class ExpencePresenter:
    """Класс, отвечающий за синхронизацию базы
    данных с расходами со списком расходов в виджете"""
    def __init__(self, window, exp_repo, cat_repo):
        self.window = window
        self.category_db = cat_repo
        self.expense_db = exp_repo
        self.expenses = self.expense_db.get_all()
        self.cats = self.category_db.get_all()
        self.cat_names= []
        for cat in self.cats:
            self.cat_names.append(cat.name)
        self.data_to_fill = []
        self.sum = 0
        for exp in self.expenses:
            attrs = []
            attrs.append(exp.added_date)
            attrs.append(str(exp.amount))
            exp_cat = self.category_db.get(exp.category).name 
            attrs.append(exp_cat)
            attrs.append(exp.expense_date)
            attrs.append(exp.comment)
            self.data_to_fill.append(attrs)
        for datas in self.data_to_fill:
            self.sum += int(datas[1])
        self.window.fill_table_data(self.data_to_fill)
        self.window.add_given_amount(str(self.sum))
        self.window.register_expense_adder(self.add_expence)
        
    def add_expence(self, amount, category, expense_date, comment):
        """Добавление расхода в базу данных по сигналу с виджета"""
        categ_index = self.cat_names.index(category)
        exp = Expense(amount, categ_index, expense_date, comment = comment)
        self.expense_db.add(exp)

app = QtWidgets.QApplication(sys.argv)
window = MyMainWindow()
wind_ruler = CategoryPresenter(window, cat_repo)
exp_manage = ExpencePresenter(window, exp_repo, cat_repo)
window.show()
sys.exit(app.exec())

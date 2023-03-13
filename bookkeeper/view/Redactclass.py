import sys
from datetime import datetime
from PySide6 import QtWidgets, QtCore, QtGui
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.view.redactmenu import RedactMenu,CommentMenu
from collections.abc import Callable

class label_widget(QtWidgets.QWidget):
    def __init__(self,text,widget,percentage, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.h1 = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(text)
        self.widg = widget
        self.h1.addWidget(self.label, percentage)
        self.h1.addWidget(self.widg, 10 - percentage)
        self.setLayout(self.h1)

def two_widgets_near(widgetone:QtWidgets.QLayout, widgettwo:QtWidgets.QWidget, percentage:float):
    h1 = QtWidgets.QHBoxLayout()
    h1.addWidget(widgetone, percentage)
    h1.addWidget(widgettwo, 10 - percentage)
    return h1
    
class MainTable(QtWidgets.QTableWidget):
    """Класс, описывающий таблицу расходов"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setColumnCount(5)
        self.setRowCount(1)
        self.setHorizontalHeaderLabels(["Дата Добавления", "Сумма", "Категория", "Дата Расхода", 
                                        "Комментарий"])
        self.setWindowTitle("Последние расходы")
        self.cur_row = 0
        self.header = self.horizontalHeader()
        self.header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            4, QtWidgets.QHeaderView.Stretch)
        self.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.verticalHeader().hide()
    
    def fill_data(self, data:list[list[str]]):
        """Заполняет таблицу начальными расходами из базы"""
        for i, row in enumerate(data):
            if i >= self.rowCount():
                self.insert_row()
            for j, x in enumerate(row):
                self.setItem(
                    i, j, 
                    QtWidgets.QTableWidgetItem(str(x))
                    )
        self.cur_row += len(data)
    
    def fill_row(self, data:list[str]):
        """Заполнение последнего ряда таблицы новым расходом"""
        for j, element in enumerate(data):
            self.setItem(
                self.cur_row, j,
                QtWidgets.QTableWidgetItem(str(element))
                )
        self.cur_row += 1
    def insert_row(self):
        """Добавления ряда к таблице в случае ее заполненности"""
        cond = True
        row_count = self.rowCount()
        column_count = self.columnCount()
        for j in range(column_count):
            if self.item(row_count, j) == True:
                cond = False
        if cond == True:
            self.insertRow(row_count)

    def remove_row(self):
        """Удаление ряда из таблицы расходов"""
        if self.rowCount() > 0:
            self.removeRow(self.rowCount() - 1)
        self.cur_row -= 1
    
    def get_last_expense_sum(self):
        """Информация о сумме последнего расхода"""
        if self.rowCount() > 0:
            return self.item(self.cur_row - 1, 1).text()
        else:
            return 0
            
class BudgetTable(QtWidgets.QTableWidget):
    """Таблица для отображения бюджета"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setColumnCount(2)
        self.setRowCount(3)   
        self.setHorizontalHeaderLabels("Сумма Бюджет".split())
        self.setVerticalHeaderLabels("День Неделя Месяц".split())
        self.setWindowTitle("Бюджет")
        self.cur_row = 0
        self.header = self.horizontalHeader()
        self.header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
        self.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.fill_with_zeros()
        
    def fill_with_zeros(self):
        """Заполнение бюджета нулями"""
        for i in range(3):
            self.setItem(
                i, 1, 
                QtWidgets.QTableWidgetItem(str(0))
                )
        for i in range(3):
            self.setItem(
                i, 0, 
                QtWidgets.QTableWidgetItem(str(0))
                )  
        
        #Заполнение редактированными данными о бюджете    
    def fill_numbers(self, day, week, month):
        """Заполнение редактированными данными о бюджете"""
        budgets = [day, week, month]
        for i in range(len(budgets)):
            self.setItem(
                i, 1, 
                QtWidgets.QTableWidgetItem(str(budgets[i]))
                )

    def add_spending(self, text:str):
        """Добавление суммы расхода в таблицу бюджета"""
        if len(text) != 0:
            amount = float(text)
            for i in range(self.rowCount()):
                cur_amount = float(self.item(i,0).text())
                self.setItem(
                    i, 0,
                    QtWidgets.QTableWidgetItem(str(cur_amount + amount))
                    )
    
    def delete_spending(self, minus:float):
        """Удаление суммы расхода из таблицы бюджета"""
        for i in range(self.rowCount()):
            cur_amount = float(self.item(i,0).text())
            self.setItem(
                i, 0,
                QtWidgets.QTableWidgetItem(str(cur_amount - minus))
                )

class CatChoice(QtWidgets.QComboBox):
    """Меню с категориями"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.combo = QtWidgets.QComboBox()
        
    def add_item(self, name:str):
        """Добавление категории"""
        self.addItem(name)
        
    def set_cats_list(self, items:list):
        """Установка изначального списка категорий из базы данных"""
        self.addItems(items)
        
    def get_cats(self):
        """Получение категорий из списка"""
        all_items = [self.itemText(i) for i in range(self.count())]
        return all_items
        
    def remove_category(self, text):
        """Удаление категории из списка"""
        for i in range(self.count()):
            if self.itemText(i) == text:
                self.removeItem(i)

class RedactField(QtWidgets.QWidget):
    """Меню редактирования(все, что находится под
    таблицей бюджета"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        
        #Поле для записи суммы покупки
        self.sum_field = QtWidgets.QLineEdit()
        self.sum_field.setValidator(QtGui.QDoubleValidator(-999999, 999999, 3))
        self.sum_widg = label_widget("Сумма", self.sum_field, 1)
        self.layout.addWidget(self.sum_widg)
        
        #Управление категориями
        self.combobox = CatChoice()
        self.choicebar = label_widget("Категория", self.combobox, 1)
        self.redbut = QtWidgets.QPushButton(text = "Редактировать")
        
        #Вариант выбора категории
        self.cats = two_widgets_near(self.choicebar, self.redbut, 7)
        self.layout.addLayout(self.cats)
        
        #Кнопка для добавления и удаления расхода
        self.mid_layout = QtWidgets.QHBoxLayout()
        self.addbut = QtWidgets.QPushButton(text = "Добавить")
        self.delbut = QtWidgets.QPushButton(text = "Удалить расход")
        self.mid_layout.addWidget(self.addbut, 7)
        self.mid_layout.addWidget(self.delbut, 3)
        self.layout.addLayout(self.mid_layout)
   
    def get_sum(self):
        """Получение введенной суммы"""
        return self.sum_field.text()
        
    def get_category(self):
        """Получение текущего выбора в меню выбора категорий"""
        return self.combobox.currentText()
        
       
class MyMainWindow(QtWidgets.QMainWindow):
    """Сборка главного окна приложения"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #главный виджет
        self.main_widget = QtWidgets.QWidget()
        
        #Таблица для внесения расходов
        self.table = MainTable()
        #Таблица для бюджета
        self.budget_table = BudgetTable()
        #Окно редактирования
        self.red_field = RedactField() 
        self.red_field.addbut.clicked.connect(self.open_comment)
        #self.red_field.delbut.clicked.connect(self.cancel_expense_in_budget)
        self.red_field.delbut.clicked.connect(self.cancel_expense)
        #self.red_field.addbut.clicked.connect(self.fill_in_table)
        self.red_field.redbut.clicked.connect(self.open_categ_menu)
       
        
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.budget_table)
        self.layout.addWidget(self.red_field)
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("The Bookkeeper App")
    
    def register_cat_adder(self, cat_adder: Callable[[Category, Category], None]):
        """Синхронизация с базой данных при добавлении категории"""
        self.cat_adder = cat_adder
        
    def add_cat_to_database(self, cat, parent):
        """Добавление категории в датабазу"""
        self.cat_adder(cat, parent)
        
    def add_category(self, name):
        """Добавление категории в таблицу категори"""
        self.red_field.combobox.add_item(name)
        
    def register_cat_deleter(self, cat_deleter: Callable[[Category], None]):
        """Синхронизация с базой данных при удалении категории"""
        self.cat_deleter = cat_deleter
        
    def delete_cat_from_database(self, cat):
        """Удаление категории из датабазы"""
        self.cat_deleter(cat)
        
    def register_expense_adder(self, exp_adder: Callable[[str, str, str, str], None]):
        """Синхронизация с базой данных при добавлении расхода"""
        self.add_exp = exp_adder
    
    def get_comment(self, comment):
        """Получение комментария при добавлении нового расхода"""
        self.comment = comment
        
    def get_expdate(self, date):
        """Получение даты расхода при добавлении нового расхода"""
        self.date = date
   
    def insert_table_row(self):
        """Добавление ряда в таблицу расходов"""
        self.table.insert_row()
        
    def fill_table_data(self, data:list[list[str]]):
        """Заполнение таблицы расходов данными"""
        self.table.fill_data(data)
        
    def add_row(self):
        """Добавление ряда с новым расходом"""
        row_data = []
        now = datetime.now()
        this_moment = now.strftime("%d/%m/%Y %H:%M:%S")
        row_data.append(this_moment)
        row_data.append(self.red_field.get_sum())
        row_data.append(self.red_field.get_category())
        row_data.append(self.date)
        row_data.append(self.comment)
        self.table.fill_row(row_data)
        self.add_exp(self.red_field.get_sum(), self.red_field.get_category(), 
                     self.date, self.comment)
                     
    def cancel_expense(self):
        """Отмена последнего расхода"""
        amount = int(self.table.get_last_expense_sum())
        self.budget_table.delete_spending(amount)
        self.table.remove_row()
    
    def set_categories(self, items:list):
        """Заполнение списка категорий"""
        self.red_field.combobox.set_cats_list(items)
        
    def redact_budget(self, day, week, month):
        """Редактирование бюджета"""
        self.budget_table.fill_numbers(day, week, month)
        
    def add_amount(self):
        """Добавление суммы нового расхода в бюджет"""
        spending = self.red_field.get_sum()
        self.budget_table.add_spending(spending)
    
    def add_given_amount(self, sum_of_spent):
        """Добавление суммы в бюджет"""
        self.budget_table.add_spending(sum_of_spent)
        
    def open_comment(self):
        """Открытие диалогового меню для добавления расхода"""
        comment = CommentMenu(self)
        comment.setWindowTitle("Добавление комментария")
        comment.exec()
    
    def open_categ_menu(self):
        """Открытие диалогового меню для изменения списка категорий"""
        menu = RedactMenu(self)
        menu.setWindowTitle("Редактирование списка категорий")
        menu.exec()

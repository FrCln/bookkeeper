import sys 

from PySide6 import QtWidgets, QtCore, QtGui

class RedactMenu(QtWidgets.QDialog):
    def __init__(self,parent = None ,*args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.mid_layout = QtWidgets.QHBoxLayout()
        self.addopt = QtWidgets.QPushButton(text = "Добавить категорию")
        self.delopt = QtWidgets.QPushButton(text = "Удалить категорию")
        self.mid_layout.addWidget(self.addopt)
        self.mid_layout.addWidget(self.delopt)
        self.layout.addLayout(self.mid_layout)
        self.budgopt = QtWidgets.QPushButton(text = "Установить бюджет")
        self.layout.addWidget(self.budgopt)
        
        self.addopt.clicked.connect(self.open_add_window)
        self.delopt.clicked.connect(self.open_del_window)
        self.budgopt.clicked.connect(self.open_budg_menu)
    
    def open_add_window(self):
        dlg = AddMenu(self)
        dlg.setWindowTitle("Добавление категории")
        dlg.exec()
 
    def open_del_window(self):
        dlg = DelMenu(self)
        dlg.setWindowTitle("Удаление категории")
        dlg.exec()
        
    def open_budg_menu(self):
        dlg = BudgetMenu(self)
        dlg.setWindowTitle("Редактирование бюджета")
        dlg.exec()
        
        
class CommentMenu(QtWidgets.QDialog):
    def __init__(self, parent = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        
        #Поле для внесения комментария
        self.mid_layout1 = QtWidgets.QHBoxLayout()
        self.label_com = QtWidgets.QLabel("Введите комментарий")
        self.comm_place = QtWidgets.QLineEdit()
        self.mid_layout1.addWidget(self.label_com)
        self.mid_layout1.addWidget(self.comm_place)
        
        #Поле для внесения даты расхода
        self.mid_layout2 = QtWidgets.QHBoxLayout()
        self.label_date = QtWidgets.QLabel("Введите дату расхода")
        self.date_place = QtWidgets.QLineEdit()
        self.mid_layout2.addWidget(self.label_date)
        self.mid_layout2.addWidget(self.date_place)
        
        self.layout.addLayout(self.mid_layout1)
        self.layout.addLayout(self.mid_layout2)
        self.but = QtWidgets.QPushButton(text = "Добавить запись")
        self.but.clicked.connect(self.move_info)
        self.but.clicked.connect(self.insert_parent_row)
        self.but.clicked.connect(self.get_to_add_row)
        self.but.clicked.connect(self.add_amount_parent)
        self.but.clicked.connect(self.close)
        self.layout.addWidget(self.but)
        
    def add_amount_parent(self):
        self.parent.add_amount()
        
    def move_info(self):
        comm_text = self.comm_place.text()
        exp_date = self.date_place.text()
        self.parent.get_comment(comm_text)
        self.parent.get_expdate(exp_date)
        
    def insert_parent_row(self):
        self.parent.insert_table_row()   
        
    def get_to_add_row(self):
        self.parent.add_row()
        
        
        
        
        
    
class AddMenu(QtWidgets.QDialog):
    def __init__(self, parent = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        #Поле для внесения названия
        self.mid_layout1 = QtWidgets.QHBoxLayout()
        self.label1 = QtWidgets.QLabel("Введите название категории")
        self.edit1 = QtWidgets.QLineEdit()
        self.mid_layout1.addWidget(self.label1)
        self.mid_layout1.addWidget(self.edit1)
        self.layout.addLayout(self.mid_layout1)
        #Поле для внесения названия родителя
        self.mid_layout2 = QtWidgets.QHBoxLayout()
        self.label2 = QtWidgets.QLabel("Введите название категории-родителя")
        self.edit2 = QtWidgets.QLineEdit()
        self.mid_layout2.addWidget(self.label2)
        self.mid_layout2.addWidget(self.edit2)
        self.layout.addLayout(self.mid_layout2)
        #Поле для утверждения изменений
        self.but = QtWidgets.QPushButton(text = "Добавить категорию")
        self.layout.addWidget(self.but)
        self.but.clicked.connect(self.add_cat_to_parent)
        self.but.clicked.connect(self.closing)
            
    def add_cat_to_parent(self):
        cat_name = self.edit1.text()
        cat_parent = self.edit2.text()
        self.parent.parent.add_category(cat_name)
        self.parent.parent.add_cat_to_database(cat_name, cat_parent)
    
        
    def closing(self):
        self.close()
        
      
class DelMenu(QtWidgets.QDialog):
    def __init__(self, parent = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.mid_layout = QtWidgets.QHBoxLayout()
        #Поле для внесения названия
        self.label = QtWidgets.QLabel("Выберите категорию для удаления")
        self.choice = QtWidgets.QComboBox()
        self.items_to_add = self.parent.parent.red_field.combobox.get_cats()
        self.choice.addItems(self.items_to_add)
        self.mid_layout.addWidget(self.label)
        self.mid_layout.addWidget(self.choice)
        self.layout.addLayout(self.mid_layout)
        self.but = QtWidgets.QPushButton(text = "Удалить категорию")
        self.layout.addWidget(self.but)
        self.but.clicked.connect(self.delete_category_in_parent)
        self.but.clicked.connect(self.closing)
        
    def delete_category_in_parent(self):
        cat_to_del = self.choice.currentText()
        self.parent.parent.red_field.combobox.remove_category(cat_to_del)
        self.parent.parent.delete_cat_from_database(cat_to_del)
        
    def closing(self):
        self.close()
        
        
class BudgetMenu(QtWidgets.QDialog):
    def __init__(self, parent = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        
        #Установление бюджета на день
        self.mid_layout_day = QtWidgets.QHBoxLayout()
        self.day_label = QtWidgets.QLabel("Введите бюджет на день")
        self.day_field = QtWidgets.QLineEdit()
        self.day_field.setValidator(QtGui.QDoubleValidator(-999999, 999999, 3))
        self.mid_layout_day.addWidget(self.day_label)
        self.mid_layout_day.addWidget(self.day_field)
        self.layout.addLayout(self.mid_layout_day)
        
        #Установление бюджета на неделю
        self.mid_layout_week = QtWidgets.QHBoxLayout()
        self.week_label = QtWidgets.QLabel("Введите бюджет на неделю")
        self.week_field = QtWidgets.QLineEdit()
        self.week_field.setValidator(QtGui.QDoubleValidator(-999999, 999999, 3))
        self.mid_layout_week.addWidget(self.week_label)
        self.mid_layout_week.addWidget(self.week_field)
        self.layout.addLayout(self.mid_layout_week)
        
        #Установление бюджета на месяц
        self.mid_layout_month = QtWidgets.QHBoxLayout()
        self.month_label = QtWidgets.QLabel("Введите бюджет на месяц")
        self.month_field = QtWidgets.QLineEdit()
        self.month_field.setValidator(QtGui.QDoubleValidator(-999999, 999999, 3))
        self.mid_layout_month.addWidget(self.month_label)
        self.mid_layout_month.addWidget(self.month_field)
        self.layout.addLayout(self.mid_layout_month)
        
        #Кнопка для подтверждения изменений
        self.but = QtWidgets.QPushButton(text = "Подтвердить изменения")
        self.layout.addWidget(self.but)
        
        self.but.clicked.connect(self.send_data_to_parent)
        self.but.clicked.connect(self.closing)
        
        
    def send_data_to_parent(self):
        day = self.day_field.text()
        week = self.week_field.text()
        month = self.month_field.text()
        self.parent.parent.redact_budget(day, week, month)
        
    def closing(self):
        self.close()
        
        
        
        
        
        

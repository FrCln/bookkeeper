import sys 

from PySide6 import QtWidgets, QtCore, QtGui

class RedactMenu(QtWidgets.QDialog):
    def __init__(self,parent = None ,*args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)
        self.addopt = QtWidgets.QPushButton(text = "Добавить категорию")
        self.delopt = QtWidgets.QPushButton(text = "Удалить категорию")
        self.layout.addWidget(self.addopt)
        self.layout.addWidget(self.delopt)
        self.addopt.clicked.connect(self.open_add_window)
        self.delopt.clicked.connect(self.open_del_window)
    
    def open_add_window(self):
        dlg = AddMenu(self)
        dlg.setWindowTitle("Добавление категории")
        dlg.exec()
 
    def open_del_window(self):
        dlg = DelMenu(self)
        dlg.setWindowTitle("Удаление категории")
        dlg.exec()
        
        
class CommentMenu(QtWidgets.QDialog):
    def __init__(self, parent = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.mid_layout = QtWidgets.QHBoxLayout()
        #Поле для внесения названия
        self.label = QtWidgets.QLabel("Введите комментарий")
        self.comm_place = QtWidgets.QLineEdit()
        self.mid_layout.addWidget(self.label)
        self.mid_layout.addWidget(self.comm_place)
        self.layout.addLayout(self.mid_layout)
        self.but = QtWidgets.QPushButton(text = "Добавить запись")
        self.but.clicked.connect(self.move_comm)
        self.but.clicked.connect(self.insert_parent_row)
        self.but.clicked.connect(self.get_to_add_row)
        self.but.clicked.connect(self.add_amount_parent)
        self.but.clicked.connect(self.close)
        self.layout.addWidget(self.but)
        
    def add_amount_parent(self):
        self.parent.add_amount()
        
    def move_comm(self):
        comm_text = self.comm_place.text()
        self.parent.get_comment(comm_text)
        
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
        self.mid_layout = QtWidgets.QHBoxLayout()
        #Поле для внесения названия
        self.label = QtWidgets.QLabel("Введите название категории")
        self.edit = QtWidgets.QLineEdit()
        self.mid_layout.addWidget(self.label)
        self.mid_layout.addWidget(self.edit)
        self.layout.addLayout(self.mid_layout)
        #Поле для утверждения изменений
        self.but = QtWidgets.QPushButton(text = "Добавить категорию")
        self.layout.addWidget(self.but)
        self.but.clicked.connect(self.add_cat_to_parent)
        self.but.clicked.connect(self.closing)
            
    def add_cat_to_parent(self):
        text = self.edit.text()
        self.parent.parent.add_category(text)
        
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
        self.but.clicked.connect(self.delete_category)
        self.but.clicked.connect(self.closing)
        
    def delete_category(self):
        cat_to_del = self.choice.currentText()
        self.parent.parent.red_field.combobox.remove_category(cat_to_del)
        
    def closing(self):
        self.close()
            
        
    

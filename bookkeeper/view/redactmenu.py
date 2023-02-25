import sys 

from PySide6 import QtWidgets, QtCore, QtGui

class RedactMenu(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)
        self.addopt = QtWidgets.QPushButton(text = "Добавить категорию")
        self.delopt = QtWidgets.QPushButton(text = "Удалить категорию")
        self.layout.addWidget(self.addopt)
        self.layout.addWidget(self.delopt)
        self.addopt.clicked.connect(self.open_add_window)
    
    def open_add_window(self):
        dlg = AddMenu(self)
        dlg.setWindowTitle("Добавление категории")
        dlg.exec()
 
        
        
        
    
class AddMenu(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        self.but.clicked.connect(self.closing)
        
    def closing(self):
        self.close()
        
        
    

import sys 

from PySide6 import QtWidgets, QtCore, QtGui

class label_widget(QtWidgets.QWidget):
    def __init__(self,text,widget, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.h1 = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(text)
        self.widg = widget
        self.h1.addWidget(self.label)
        self.h1.addWidget(self.widg)
        self.setLayout(self.h1)
    
def two_widgets_near(widgetone:QtWidgets.QLayout, widgettwo:QtWidgets.QWidget) -> QtWidgets.QHBoxLayout:
    h1 = QtWidgets.QHBoxLayout()
    h1.addWidget(widgetone)
    h1.addWidget(widgettwo)
    return h1
    
    
class MainTable(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)
    	self.setColumnCount(4)
    	self.setRowCount(20)
    	self.setHorizontalHeaderLabels("Дата Сумма Категория Комментарий".split())
    	self.setWindowTitle("Последние расходы")
    	
    	
    
class CatChoice(QtWidgets.QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.combo = QtWidgets.QComboBox()

class RedactField(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        #Поле для записи суммы покупки
        self.sum_field = QtWidgets.QLineEdit()
        self.sum_field.setValidator(QtGui.QDoubleValidator(-999999, 999999, 3))
        self.sum_widg = label_widget("Сумма", self.sum_field)
        self.layout.addWidget(self.sum_widg)
        #Управление категориями
        self.combobox = CatChoice()
        self.choicebar = label_widget("Категория", self.combobox)
        self.redbut = QtWidgets.QPushButton(text = "Редактировать")
        #Вариант выбора категории
        self.cats = two_widgets_near(self.choicebar, self.redbut)
        self.layout.addLayout(self.cats)
        #Кнопка для добавлени
        self.addbut = QtWidgets.QPushButton(text = "Добавить")
        self.layout.addWidget(self.addbut)
        self.addbut.clicked.connect(self.print_sum)
        
    def print_sum(self):
        print(self.sum_field.text())  
        
    def get_sum(self):
        return self.sum_field.text()
            
    def is_filled(self):
        return bool(self.sum_field.text()) 
        
        
        
	
app = QtWidgets.QApplication(sys.argv)

window = QtWidgets.QMainWindow()
main_widget = QtWidgets.QWidget()
window.setCentralWidget(main_widget)

table_widget = MainTable()
redact_widget = RedactField()

vertical_layout = QtWidgets.QVBoxLayout()
vertical_layout.addWidget(table_widget)
vertical_layout.addWidget(redact_widget)
main_widget.setLayout(vertical_layout)

window.setWindowTitle('The Bookkeeper App')
#window.resize(300,100)
window.show()
sys.exit(app.exec())

import sys 

from PySide6 import QtWidgets, QtCore, QtGui

app = QtWidgets.QApplication(sys.argv)

window = QtWidgets.QMainWindow()

main_widget = QtWidgets.QWidget()
window.setCentralWidget(main_widget)

vertical_layout = QtWidgets.QVBoxLayout()
expence_table = QtWidgets.QTableWidget(20, 4) 
expence_table.setHorizontalHeaderLabels("Дата Сумма Категория Комментарий".split())

vertical_layout.addWidget(expence_table)
btn = QtWidgets.QPushButton(window, text = "Бухгалтер")
vertical_layout.addWidget(btn)
main_widget.setLayout(vertical_layout)
window.setWindowTitle('The Bookkeeper App')
window.resize(300, 100)
window.show()
sys.exit(app.exec())

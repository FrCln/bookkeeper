import sys 

from PySide6 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.MainWindow()
btn = QtWidgets.QPushButton(window, text = "Бухгалтер")
window.setWindowTitle('The Bookkeeper App')
window.resize(300, 100)
window.show()
sys.exit(app.exec())

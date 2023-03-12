"""
Widget of editing pane
"""

from PySide6 import QtWidgets
from PySide6.QtWidgets import (QWidget, QComboBox)

from .edit_ctg_window import EditCtgWindow


def set_data(box: QComboBox, cats: list[str]) -> None:
    for cat in cats:
        box.addItem(cat)


class EditWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Редактирование")
        layout.addWidget(message)

        sum_label = QtWidgets.QLabel("Сумма")
        cat_label = QtWidgets.QLabel("Категория")
        add_button = QtWidgets.QPushButton("Добавить")
        cat_edit_button = QtWidgets.QPushButton("Редактировать")
        sum_line = QtWidgets.QLineEdit("0")
        cats_box = QtWidgets.QComboBox()
        glayout = QtWidgets.QGridLayout()

        glayout.addWidget(sum_label, 0, 0)
        glayout.addWidget(sum_line, 0, 1)
        glayout.addWidget(cat_label, 1, 0)
        glayout.addWidget(cats_box, 1, 1)
        glayout.addWidget(cat_edit_button, 1, 2)
        glayout.addWidget(add_button, 2, 1)
        gwidget = QWidget()
        gwidget.setLayout(glayout)
        layout.addWidget(gwidget)

        self.cat_list = ["Продукты", "Книги"]
        set_data(cats_box, self.cat_list)
        
        cat_edit_button.clicked.connect(self.open_window)

        self.setLayout(layout)
    
    def open_window(self):
        self.edit_ctg = EditCtgWindow(self.cat_list)
        self.edit_ctg.show()


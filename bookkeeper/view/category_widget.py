"""
Модуль содержит класс виджета категорий для отображения информации о категориях деревом.
"""
from PyQt6.QtWidgets import (
    QTreeWidget,
    QTreeWidgetItem,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLineEdit,
)


class CategoryWidget(QWidget):
    """
    Виджет для отображения дерева категорий.
    """
    def __init__(self) -> None:
        super().__init__()

        # просто для примера
        self.categories = [
            {"name": "Food", "subcategories": ["Groceries", "Restaurants"]},
            {"name": "Transportation", "subcategories": ["Gas", "Parking", "Tolls"]},
            {"name": "Entertainment", "subcategories": ["Movies", "Concerts", "Sports"]},
            {"name": "Housing", "subcategories": ["Rent", "Mortgage"]},
            {"name": "Other", "subcategories": []}
        ]

        # создаёт QTreeWidget для отображения списка категорий
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Categories")
        self.tree.setColumnCount(2)
        self.tree.setHeaderHidden(True)

        # заполняет дерево данными категорий
        for category in self.categories:
            parent = QTreeWidgetItem(self.tree, [category["name"], ""])
            for subcategory in category["subcategories"]:
                child = QTreeWidgetItem(parent, [subcategory, ""])

        # кнопка для добавления новой категории
        add_button = QPushButton("Add Category")

        # кнопка для удаления категории
        delete_button = QPushButton("Delete Category")

        # line для редактирования имени категории
        name_edit = QLineEdit()

        # лейаут для размещения кнопок и редактирования строки
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(name_edit)

        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        layout.addLayout(button_layout)
        self.setLayout(layout)

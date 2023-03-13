"""
Модуль содержит класс виджета категорий для отображения информации о категориях списком.
"""
from typing import List

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLineEdit,
)


class Signal:
    pass


class CategoryWidget(QWidget):
    """
    Виджет для отображения списка категорий.
    """
    category_name_edited = pyqtSignal(str, str)
    delete_category_signal = pyqtSignal(str)
    add_category_signal = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

        self.setup_ui()

    def setup_ui(self) -> None:
        """
        Устанавливает интерфейс для отображения категорий
        """
        # создаёт QListWidget для отображения списка категорий
        self.list = QListWidget()

        # line для редактирования имени категории
        self.name_edit = QLineEdit()

        # кнопка для добавления новой категории
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.on_add_button_clicked)

        # кнопка для удаления категории
        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.on_delete_button_clicked)

        # лейаут для размещения кнопок и редактирования строки
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.name_edit)

        # создаём QVBoxLayout и добавляем QListWidget и button_layout в него
        layout = QVBoxLayout()
        layout.addWidget(self.list)
        layout.addLayout(button_layout)

        # устанавливаем созданный QVBoxLayout в качестве layout для CategoryWidget
        self.setLayout(layout)

        # подключаем слот для редактирования категории при двойном клике
        self.list.itemDoubleClicked.connect(self.on_item_double_clicked)

        # подключаем слот для проверки текста в QLineEdit
        self.name_edit.textChanged.connect(self.on_name_edit_changed)

        # отключает кнопку добавления
        self.add_button.setEnabled(False)

    def init_category_list(self, categories: List[str]) -> None:
        """
        Инициализирует список, на котором будут
        отображаться данные о категориях.
        """
        self.list.clear()

        # сортирует категории по алфавиту
        categories = sorted(categories)

        # проверяет существование категория "Удалено"
        if "Удалено" in categories:
            categories.remove("Удалено")
            categories.append("Удалено")

        for category_name in categories:
            item = QListWidgetItem(category_name)
            self.list.addItem(item)

    def on_add_button_clicked(self) -> None:
        """
        Добавляет новую строку в список, ЕСЛИ текстовое поле
        не пустое и не содержит дубликатов.
        """
        name = self.name_edit.text()
        if name:
            # проверяет нет ли категории в списке
            categories = [self.list.item(i).text() for i in range(self.list.count())]
            if name not in categories:
                self.add_category_signal.emit(name)
            self.name_edit.clear()

    def on_delete_button_clicked(self) -> None:
        """
        Удаляет элементы из таблицы
        """
        selected_items = self.list.selectedItems()
        for item in selected_items:
            category_name = item.text()
            self.delete_category_signal.emit(category_name)
            self.list.takeItem(self.list.row(item))

    def on_editing_finished(self, line_edit: QLineEdit,
                            item: QListWidgetItem) -> None:
        """
        Заменяет старый текст элемента списка новым текстом,
        введенным в редактировании строки.
        """
        # получаем новое имя категории
        new_text = line_edit.text()

        # получаем старое имя категории
        old_text = item.text()

        # удаляем редактирующийся элемент
        self.list.removeItemWidget(item)

        # обновляем элемент списка
        item.setText(new_text)

        # эмитируем сигнал, что имя категории изменилось
        self.category_name_edited.emit(old_text, new_text)

    def on_item_double_clicked(self, item: QListWidgetItem) -> None:
        """
        Создаёт виджет редактирования строки для
        выбранного элемента
        """
        if item is not None:
            # получаем текст выбранного элемента
            text = item.text()

            # создаём line edit для редактирования текста
            line_edit = QLineEdit(text)
            line_edit.editingFinished.connect(lambda:
                                              self.on_editing_finished
                                              (line_edit, item))

            # заменяем выбранный элемент на line edit
            self.list.setItemWidget(item, line_edit)

            # выделяем весь текст в line edit
            line_edit.selectAll()

            # устанавливаем фокус на line edit
            line_edit.selectAll()
            line_edit.setFocus()

    def on_name_edit_changed(self, text: str) -> None:
        """
        Включает или отключает кнопку в зависимости от того
        пустое текстовое поле или нет
        """
        self.add_button.setEnabled(bool(text))

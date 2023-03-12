"""
Модуль содержит класс виджета категорий для отображения информации о категориях списком.
"""
from PyQt6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLineEdit,
)


class CategoryWidget(QWidget):
    """
    Виджет для отображения списка категорий.
    """

    def __init__(self) -> None:
        super().__init__()

        # просто для примера
        self.categories = [
            "Еда",
            "Транспорт",
            "Развлечения",
            "Дом",
            "Другое"
        ]

        self.setup_ui()

    def setup_ui(self) -> None:
        """
        Устанавливает интерфейс для отображения категорий
        """
        # создаёт QListWidget для отображения списка категорий
        self.list = QListWidget()

        # заполняет список данными категорий
        self.list.addItems(self.categories)

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

    def on_add_button_clicked(self) -> None:
        """
        Добавляет новую строку в список, ЕСЛИ текстовое поле
        не пустое и не содержит дубликатов.
        """
        name = self.name_edit.text()
        if name:
            # проверяет нет ли категории в списке
            categories = [self.list.item(i).text() for i in range(self.list.count())]
            print(categories)
            if name not in categories:
                self.list.addItem(name)
            self.name_edit.clear()

    def on_delete_button_clicked(self) -> None:
        """
        Удаляет элементы из таблицы
        """
        selected_items = self.list.selectedItems()
        for item in selected_items:
            self.list.takeItem(self.list.row(item))

    def on_editing_finished(self, line_edit: QLineEdit,
                            item: QListWidgetItem) -> None:
        """
        Заменяет старый текст элемента списка новым текстом,
        введенным в виджете редактирования строк.
        """
        # получаем новый текст из line edit
        new_text = line_edit.text()

        # заменяем элемент списка на новый текст
        index = self.list.row(item)
        self.list.takeItem(index)
        self.list.insertItem(index, new_text)

        # удаляем line edit
        line_edit.deleteLater()

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
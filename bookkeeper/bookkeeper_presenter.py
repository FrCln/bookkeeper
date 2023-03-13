from datetime import datetime, timedelta

from PyQt6.QtWidgets import QMessageBox

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense

from bookkeeper.repository.abstract_repository import AbstractRepository

from bookkeeper.view.main_window import MainWindow


class Presenter:
    """
    Presenter Bookkeeper, связывает MODEL и VIEW.
    """

    def __init__(self, exp_repo: AbstractRepository[Expense],
                 cat_repo: AbstractRepository[Category], bud_repo: AbstractRepository[Budget]) -> None:
        self.cat_repo = cat_repo
        self.exp_repo = exp_repo
        self.bud_repo = bud_repo

    def show_main_window(self):
        self.main_window = MainWindow()

        # инициализирует таблицу расходов
        self.init_table()

        # инициализирует список категорий
        self.init_category()

        self.init_budget()

        # соединяем сигналы
        self.main_window.expenses_list_widget.delete_button_clicked.connect(self.delete_expense)
        self.main_window.add_expense_widget.expense_added.connect(self.add_expense)
        self.main_window.expenses_list_widget.category_cell_double_clicked.connect(
            self._on_category_cell_double_clicked)
        self.main_window.expenses_list_widget.category_cell_changed.connect(self._on_category_cell_changed)
        self.main_window.expenses_list_widget.expense_cell_changed.connect(self.update_expense)
        self.main_window.category_widget.category_name_edited.connect(self.update_category_name)
        self.main_window.category_widget.delete_category_signal.connect(self.delete_category)
        self.main_window.category_widget.add_category_signal.connect(self.add_category)

        self.main_window.budget_widget.day_budget_edited.connect(self.update_day_budget)
        self.main_window.budget_widget.week_budget_edited.connect(self.update_week_budget)
        self.main_window.budget_widget.month_budget_edited.connect(self.update_month_budget)

        self.get_expenses_for_today()

        # обновление таблицы расходов и категорий
        self.update_expenses_list()
        self.update_category_list()

        self.main_window.show()

    def init_table(self) -> None:
        self.main_window.expenses_list_widget.init_table()

    def init_category(self) -> None:
        categories = [category.name for category in self.cat_repo.get_all()]
        self.main_window.category_widget.list.clear()
        self.main_window.category_widget.init_category_list(categories)

    def update_expenses_list(self) -> None:
        """
        Обновляет содержимое таблицы расходов
        на основе данных из репозитория.
        """
        categories = self.cat_repo.get_all()
        objects = self.exp_repo.get_all()
        expenses = [expense for expense in objects if isinstance(expense, Expense)]
        expenses_dict = []
        categories_dict = {}

        # Ищем категорию "Удалено" и получаем её pk
        deleted_category_pk = None
        for deleted_category in categories:
            if deleted_category.name == "Удалено":
                deleted_category_pk = deleted_category.pk
                break

        if deleted_category_pk is None:
            deleted_category = Category(name="Удалено")
            self.cat_repo.add(deleted_category)

        # сопоставляем объекты Expense со словарём в виджете
        for expense in expenses:
            category = categories_dict.get(expense.category)
            if category is None:
                category = self.cat_repo.get(expense.category)
                if category is None:
                    # приписываем запись к категории «Удалено»
                    category = deleted_category
                    expense.category = category.pk
                    self.exp_repo.update(expense)
                categories_dict[expense.category] = category

            expense_dict = {
                "date": datetime.strptime(expense.expense_date, "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d"),
                "description": expense.comment,
                "category": str(category.name),
                "amount": str(expense.amount)
            }
            expenses_dict.append(expense_dict)

        self.main_window.expenses_list_widget.update_table(expenses_dict)

    def delete_expense(self, index: int) -> None:
        """
        Удаляет расход из базы данных и обновляет содержимое таблицы.
        """
        try:
            objects = self.exp_repo.get_all()
            expenses = [expense for expense in objects if isinstance(expense, Expense)]
            expense = expenses[index]
            self.exp_repo.delete(expense.pk)
            self.update_expenses_list()
            self.get_expenses_for_today()
        except Exception as e:
            print(f"Ошибка delete_expense: {e}")

    def update_category_list(self) -> None:
        """
        Обновляет содержимое списка категорий в комбобоксе виджета добавления расхода
        на основе данных из репозитория.
        """
        categories = self.cat_repo.get_all()
        categories_list = [(category.pk, category.name) for category in categories]
        self.main_window.add_expense_widget.set_categories(categories_list)

    def _on_category_cell_double_clicked(self, row: int, column: int, category_name: str) -> None:
        categories = self.cat_repo.get_all()
        categories = [(category.pk, category.name) for category in categories]
        self.main_window.expenses_list_widget._update_category_cell(row, column, categories)

    def _on_category_cell_changed(self, row: int, column: int, category_id: int) -> None:
        expense_id = self.exp_repo.get_all()[row].pk
        expense = self.exp_repo.get(expense_id)
        category = self.cat_repo.get(category_id)

        try:
            msg_box = QMessageBox()
            msg_box.setText(f"Вы действительно хотите изменить категорию на {category.name}?")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg_box.setDefaultButton(QMessageBox.StandardButton.No)
            yes_button = msg_box.button(QMessageBox.StandardButton.Yes)
            yes_button.setText("Да")
            no_button = msg_box.button(QMessageBox.StandardButton.No)
            no_button.setText("Нет")
            ret = msg_box.exec()
            if ret == QMessageBox.StandardButton.Yes:
                expense.category = category_id
                self.exp_repo.update(expense)
                self.update_expenses_list()
            else:
                self.update_expenses_list()

        except Exception as e:
            print(f"Ошибка _on_category_cell_changed: {e}")

    def add_expense(self) -> None:
        """
        Создает новый объект Expense на основе данных из виджета
        AddExpenseWidget и добавляет его в репозиторий. Обновляет
        содержимое таблицы расходов.
        """
        comment = self.main_window.add_expense_widget.description_edit.text()
        # для поиска pk категории на основе названия:
        category_name = self.main_window.add_expense_widget.category_combo.currentText()
        category_id = next((id for id, name in self.main_window.add_expense_widget.categories if name == category_name),
                           None)
        amount = self.main_window.add_expense_widget.amount_edit.text()

        expense = Expense(amount, category_id, datetime.now(), datetime.now(), comment)
        try:
            self.exp_repo.add(expense)
            self.update_expenses_list()
            self.get_expenses_for_today()
        except Exception as e:
            print(f"Ошибка add_expense: {e}")

    def update_expense(self, row: int, column: int, new_value: str) -> None:
        objects = self.exp_repo.get_all()
        expenses = [expense for expense in objects if isinstance(expense, Expense)]
        expense = expenses[row]
        if column == 1:
            expense.amount = int(new_value)
        elif column == 2:
            expense.expense_date = datetime.strptime(new_value, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S.%f')
        elif column == 3:
            expense.comment = new_value
        try:
            self.exp_repo.update(expense)
            self.update_expenses_list()
        except Exception as e:
            print(f"Ошибка update_expense: {e}")

    def update_category_name(self, old_name: str, new_name: str):
        """
        Обновляет имя категории в репозитории категорий.
        """
        try:
            # Получаем список всех категорий из репозитория
            categories = self.cat_repo.get_all()

            # Ищем категорию с нужным именем и получаем ее pk
            category_pk = None
            for category in categories:
                if category.name == old_name:
                    category_pk = category.pk
                    break

            if category_pk is None:
                QMessageBox.critical(None, 'Ошибка', f'Категория "{old_name}" не найдена.')
                return

            # Создаем экземпляр Category с новым именем и старым pk и parent
            old_category = self.cat_repo.get(category_pk)
            new_category = Category(name=new_name, pk=old_category.pk, parent=old_category.parent)
            self.cat_repo.update(new_category)
        except Exception as e:
            print(f"Ошибка update_category_name: {e}")
        # обновление таблицы расходов и категорий
        self.update_expenses_list()
        self.update_category_list()
        self.init_category()

    def delete_category(self, category_name: str):
        """
        Удаляет категорию из репозитория категорий и
        обновляет таблицу расходов и список категорий.
        """
        print(category_name)
        try:
            # Получаем список всех категорий из репозитория
            categories = self.cat_repo.get_all()

            # Ищем категорию с нужным именем и получаем её pk
            category_pk = None
            for category in categories:
                if category.name == category_name:
                    category_pk = category.pk
                    break

            if category_pk is None:
                QMessageBox.critical(None, 'Ошибка', f'Категория "{category_name}" не найдена.')
                return

            self.cat_repo.delete(category_pk)

            # обновление таблицы расходов и категорий
            self.update_expenses_list()
            self.update_category_list()
        except Exception as e:
            print(f"Ошибка delete_category: {e}")

    def add_category(self, category_name: str) -> None:
        """
        Добавляет новую категорию
        """
        category = Category(name=category_name)
        self.cat_repo.add(category)
        self.update_expenses_list()
        self.update_category_list()
        self.init_category()

    def update_day_budget(self, amount: float) -> None:
        """
        Обновляет или добавляет сумму дневного бюджета
        """
        today = datetime.now().date()
        today_str = today.strftime("%Y-%m-%d %H:%M:%S")
        budget = self.bud_repo.get_all({'period': 'day', 'term': today_str})

        if budget:
            budget = budget[0]
            budget.amount = amount
            budget.period = "day"
            self.bud_repo.update(budget)
        else:
            budget = Budget.create_for_current_day(amount, self.bud_repo)

        self.main_window.budget_widget.day_budget_label.setText(f"\u20bd{amount:.2f}")

    def update_week_budget(self, amount: float) -> None:
        """
        Обновляет или добавляет сумму недельного бюджета
        """
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        days_since_monday = today.isoweekday() - 1
        week_start = (today - timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)
        budget = self.bud_repo.get_all({'period': 'week', 'term': week_start})

        if budget:
            budget = budget[0]
            budget.amount = amount
            budget.period = "week"
            print(budget)
            self.bud_repo.update(budget)
        else:
            budget = Budget.create_for_current_week(amount, self.bud_repo)

        self.main_window.budget_widget.week_budget_label.setText(f"\u20bd{amount:.2f}")

    def update_month_budget(self, amount: float) -> None:
        """
        Обновляет или добавляет сумму месячного бюджета
        """
        term = datetime.now().replace(day=1)
        budgets = self.bud_repo.get_all({'period': 'month'})
        budget = next((b for b in budgets if
                       datetime.strptime(b.term, '%Y-%m-%d %H:%M:%S.%f').month == term.month and datetime.strptime(
                           b.term,
                           '%Y-%m-%d %H:%M:%S.%f').year == term.year),
                      None)

        if budget:
            budget.amount = amount
            budget.period = "month"
            self.bud_repo.update(budget)
        else:
            budget = Budget.create_for_current_month(amount, self.bud_repo)

        self.main_window.budget_widget.month_budget_label.setText(f"\u20bd{amount:.2f}")

    def init_budget(self):
        """
        Устанавливает значения из базы данных
        """
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today - timedelta(days=today.weekday())
        current_month = datetime.now().replace(day=1)
        day_budget = self.bud_repo.get_all({'period': 'day', 'term': today})
        week_budget = self.bud_repo.get_all({'period': 'week', 'term': week_start})
        month_budget = self.bud_repo.get_all({'period': 'month'})
        month_amount = next((b for b in month_budget if
                       datetime.strptime(b.term, '%Y-%m-%d %H:%M:%S.%f').month == current_month.month and datetime.strptime(
                           b.term,
                           '%Y-%m-%d %H:%M:%S.%f').year == current_month.year),
                      None)

        if day_budget:
            self.main_window.budget_widget.day_budget_label.setText(f"\u20bd{day_budget[0].amount:.2f}")
        if week_budget:
            self.main_window.budget_widget.week_budget_label.setText(f"\u20bd{week_budget[0].amount:.2f}")
        if month_amount:
            self.main_window.budget_widget.set_month_budget(month_amount.amount)

    def get_expenses_for_today(self):
        """
        Получает все расходы за сегодня и считает их сумму
        """
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_expenses = self.exp_repo.get_all(where={'strftime("%Y-%m-%d", expense_date)': str(today.date())})
        total_amount_today = sum(float(expense.amount) for expense in today_expenses)

        month_expenses = self.exp_repo.get_all(where={'strftime("%Y-%m", expense_date)': today.strftime("%Y-%m")})
        total_amount_month = sum(float(expense.amount) for expense in month_expenses)

        days_since_monday = today.isoweekday() - 1
        week_start = (today - timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)
        week_expenses = self.exp_repo.get_all({'strftime("%Y-%m-%d", expense_date)': str(week_start.date())})
        total_amount_week = sum(float(expense.amount) for expense in week_expenses)

        day_expenses = total_amount_today
        week_expenses = total_amount_week
        month_expenses = total_amount_month

        self.main_window.budget_widget.expenses_updated.emit(day_expenses, week_expenses, month_expenses)

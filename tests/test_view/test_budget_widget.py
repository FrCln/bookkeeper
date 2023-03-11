"""
Здесь содержатся тесты для виджета бюджета
"""
import pytest

from bookkeeper.view.budget_widget import BudgetWidget


@pytest.fixture
def budget_widget(qtbot):
    widget = BudgetWidget()
    qtbot.addWidget(widget)
    return widget


def test_budget_widget_initial_state(budget_widget):
    assert budget_widget.budget_label.text() == "Текущий бюджет: \u20bd0.00"
    assert budget_widget.day_button.isChecked()
    assert budget_widget.budget_spinbox.value() == 0.0


def test_budget_widget_update_budget_label(qtbot, budget_widget):
    budget_widget.budget_spinbox.setValue(1000.0)
    qtbot.wait(500)
    assert budget_widget.budget_label.text() == "Текущий бюджет (День): \u20bd33.33"

    budget_widget.week_button.setChecked(True)
    qtbot.wait(500)
    assert budget_widget.budget_label.text() == "Текущий бюджет (Неделя): \u20bd142.86"

    budget_widget.month_button.setChecked(True)
    qtbot.wait(500)
    assert budget_widget.budget_label.text() == "Текущий бюджет (Месяц): \u20bd1000.00"


def test_budget_widget_apply_budget(qtbot, budget_widget):
    budget_widget.budget_spinbox.setValue(2000.0)
    qtbot.wait(500)
    assert budget_widget.budget_label.text() == "Текущий бюджет (День): \u20bd66.67"

    budget_widget.week_button.setChecked(True)
    qtbot.wait(500)
    assert budget_widget.budget_label.text() == "Текущий бюджет (Неделя): \u20bd285.71"

    budget_widget.month_button.setChecked(True)
    qtbot.wait(500)
    assert budget_widget.budget_label.text() == "Текущий бюджет (Месяц): \u20bd2000.00"

    budget_widget.budget_spinbox.setValue(5000.0)
    budget_widget.apply_budget()
    qtbot.wait(500)
    assert budget_widget.budget_label.text() == "Текущий бюджет (Месяц): \u20bd5000.00"

import pytest
from pytestqt.qt_compat import qt_api

from bookkeeper.models.budget import Budget
from bookkeeper.view.category_edit import CategoryEditWindow


@pytest.fixture
def get_callback():
    def callback(val1: str) -> None:
        callback.val1 = val1

    return callback


def test_set_text(qtbot):
    widget = CategoryEditWindow()
    qtbot.addWidget(widget)

    text = "text"
    widget.set_text(text)

    assert widget.self_layout.text_edit.toPlainText() == text


def test_set_save_callback(qtbot, get_callback):
    widget = CategoryEditWindow()
    qtbot.addWidget(widget)

    widget.set_save_callback(get_callback)

    assert get_callback == widget.self_layout.save_callback


def test_button_click(qtbot, get_callback):
    widget = CategoryEditWindow()
    qtbot.addWidget(widget)

    widget.set_text("big\ntext")
    widget.set_save_callback(get_callback)
    qtbot.mouseClick(widget.self_layout.update_button, qt_api.QtCore.Qt.MouseButton.LeftButton)

    assert get_callback.val1 == widget.self_layout.text_edit.toPlainText()

"""Module responsible for entry point of UI application.
"""

import sys

from PySide6 import QtWidgets
from bookkeeper.view.main_window import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

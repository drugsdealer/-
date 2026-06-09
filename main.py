import sys
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from database.db_manager import init_database
from ui.login_window import LoginWindow
from ui.styles import APP_STYLE

RESOURCES_DIR = os.path.join(os.path.dirname(__file__), "resources")


def main():
    init_database()

    app = QApplication(sys.argv)
    app.setApplicationName("Система управления магазином")
    app.setStyleSheet(APP_STYLE)

    icon_path = os.path.join(RESOURCES_DIR, "icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = LoginWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

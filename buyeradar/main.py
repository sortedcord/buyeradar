from screens.mainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

# Code to display the main window. 
# This is the entry point of the application.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.setupUi()
    sys.exit(app.exec_())

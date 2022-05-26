from screens.mainWindow import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.setupUi()
    sys.exit(app.exec_())
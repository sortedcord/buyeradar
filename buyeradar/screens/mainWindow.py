from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5 import QtGui


from func import fetch_amazon_html, scrape_html

from components.result_card import ResultCard


CONSOLE_TEXT = ""
CONSOLE = None


class MainWindow(QMainWindow):
    def update_bar(self, value):
        if self.progressBar.value()< 100:
            self.progressBar.setProperty("value",self.progressBar.value()+value)

    def search_button_clicked(self):
        for i in reversed(range(self.verticalLayout_2.count())): 
            self.verticalLayout_2.itemAt(i).widget().setParent(None)

        global CONSOLE, CONSOLE_TEXT
        CONSOLE_TEXT += "Search Button Clicked \n"
        CONSOLE.setPlainText(CONSOLE_TEXT)

        search_query = self.search_query_textbox.toPlainText()
        CONSOLE_TEXT += f"Search Query Set as {search_query}\n\n"
        pg_val = self.progressBar.setProperty
        pg_val('value',0)
        soup = fetch_amazon_html(search_query, self)
        results = scrape_html(soup, self)
        pg_val('value', 100)
       

        for result in results:
            card = ResultCard(result)
            self.verticalLayout_2.addWidget(card)
            

        

    def setupUi(self):
        global CONSOLE_TEXT, CONSOLE

        # Creation of the Application UI
        self.resize(805, 719)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.frame = QFrame(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 75))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, -1, 0, -1)
        self.search_query_textbox = QTextEdit(self.frame)
        self.search_query_textbox.setMinimumSize(QtCore.QSize(0, 34))
        self.search_query_textbox.setMaximumSize(QtCore.QSize(16777215, 34))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.search_query_textbox.setFont(font)
        self.horizontalLayout.addWidget(self.search_query_textbox)
        self.comboBox = QComboBox(self.frame)
        self.comboBox.setMinimumSize(QtCore.QSize(175, 34))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.search_button = QPushButton(self.frame)
        self.search_button.setMinimumSize(QtCore.QSize(0, 34))
        self.horizontalLayout.addWidget(self.search_button)
        self.verticalLayout.addWidget(self.frame)
        self.verticalLayout.addWidget(self.frame)
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 781, 324))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.console_log = QPlainTextEdit(self.centralwidget)
        self.console_log.setEnabled(True)
        self.console_log.setMaximumSize(QtCore.QSize(16777215, 200))
        self.console_log.setFrameShadow(QFrame.Sunken)
        self.console_log.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)
        self.console_log.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents)
        self.console_log.setReadOnly(True)
        self.console_log.setBackgroundVisible(False)
        self.console_log.setCenterOnScroll(True)
        self.console_log.setPlaceholderText("")
        self.verticalLayout.addWidget(self.console_log)
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.verticalLayout.addWidget(self.progressBar)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 805, 26))
        self.menuFile = QMenu(self.menubar)
        self.menuSettings = QMenu(self.menubar)
        self.menuAbout = QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.actionQuit = QAction(self)
        self.actionShow_Logs = QAction(self)
        self.actionShow_Logs.setCheckable(True)
        self.menuFile.addAction(self.actionQuit)
        self.menuSettings.addAction(self.actionShow_Logs)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.show()

        # Translation of UI Elements

        CONSOLE_TEXT += "Created UI successfully\n"

        self.setWindowTitle("Product $ Tracker")
        self.search_query_textbox.setPlaceholderText(
            "Enter Product URL or Search Query")
        self.comboBox.setItemText(0, "Relevance")
        self.comboBox.setItemText(1, "Price: High to Low")
        self.comboBox.setItemText(2, "Price: Low to High")
        self.search_button.setText("Search")
        self.menuFile.setTitle("File")
        self.menuSettings.setTitle("Settings")
        self.menuAbout.setTitle("About")
        self.actionQuit.setText("Quit")
        self.actionShow_Logs.setText("Show Logs")

        CONSOLE_TEXT += "Product $ Tracker v0.0.1 \nLoaded Application Successfully\n"
        self.console_log.setPlainText(CONSOLE_TEXT)
        CONSOLE = self.console_log
        CONSOLE_TEXT = self.console_log.toPlainText()

        self.search_button.clicked.connect(self.search_button_clicked)




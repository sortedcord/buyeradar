from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5 import QtGui


from func import fetch_amazon_html, scrape_html

from components.result_card import ResultCard



class MainWindow(QMainWindow):
    def update_bar(self, value):
        if self.progressBar.value()< 100:
            self.progressBar.setProperty("value",self.progressBar.value()+value)

    def search_button_clicked(self):
        search_query = self.search_query_textbox.toPlainText()

        # Validating search query to be blank or not
        if search_query is None or search_query == "" or search_query.isspace():
            self.updateConsole("Search query cannot be blank")

        else:
            self.updateConsole(f"Search Query set as {search_query}")

            # Remove all exisiting results
            for i in reversed(range(self.result_area_vertical_layout.count())): 
                self.result_area_vertical_layout.itemAt(i).widget().setParent(None)

            pg_val = self.progressBar.setProperty
            pg_val('value',0)
            soup = fetch_amazon_html(search_query, self,debugfile="test.txt")
            results = scrape_html(soup, self)
            pg_val('value', 100)

            # Show results
            self.updateConsole("Creating Result Cards")
            QApplication.processEvents()
            i = 0
            for result in results:
                card = ResultCard(result)
                self.result_area_vertical_layout.addWidget(card)
                i+=1

        

    def setupUi(self):
        self.CONSOLE_TEXT = ""

        self.setWindowTitle("Buyeradar")

        # Creation of the Application UI
        self.resize(805, 719)

        # Central Widget
        self.centralwidget = QWidget(self)

        # Central Widget Layout 
        self.central_vertical_layout = QVBoxLayout(self.centralwidget)

        # Tab Widget
        self.tabWidget = QTabWidget(self.centralwidget)
        self.central_vertical_layout.addWidget(self.tabWidget)


        """
        ███████ ███████  █████  ██████   ██████ ██   ██ 
        ██      ██      ██   ██ ██   ██ ██      ██   ██ 
        ███████ █████   ███████ ██████  ██      ███████ 
             ██ ██      ██   ██ ██   ██ ██      ██   ██ 
        ███████ ███████ ██   ██ ██   ██  ██████ ██   ██ 
        """

        self.search_tab = QWidget()
        self.search_tab_vertical_layout = QVBoxLayout(self.search_tab)
        self.search_tab_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.search_tab_vertical_layout.setSpacing(0)
        self.tabWidget.addTab(self.search_tab, "Search")

        self.search_tab_frame = QFrame(self.search_tab)
        self.search_tab_frame.setMaximumSize(QtCore.QSize(16777215, 75))
        self.search_tab_frame.setFrameShape(QFrame.StyledPanel)
        self.search_tab_frame.setFrameShadow(QFrame.Raised)
        self.search_tab_vertical_layout.addWidget(self.search_tab_frame)

        # Search Controls
        self.horizontalLayout = QHBoxLayout(self.search_tab_frame)
        self.horizontalLayout.setContentsMargins(9, -1, 9, -1)

        self.search_query_textbox = QTextEdit(self.search_tab_frame)
        self.search_query_textbox.setMinimumSize(QtCore.QSize(0, 34))
        self.search_query_textbox.setMaximumSize(QtCore.QSize(16777215, 34))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.search_query_textbox.setFont(font)
        self.horizontalLayout.addWidget(self.search_query_textbox)

        self.comboBox = QComboBox(self.search_tab_frame)
        self.comboBox.setMinimumSize(QtCore.QSize(175, 34))
        
        self.comboBox.setFont(font)
        self.comboBox.addItem("Relevence")
        self.comboBox.addItem("Price: High to Low")
        self.comboBox.addItem("Price: Low to High")
        self.horizontalLayout.addWidget(self.comboBox)

        self.search_button = QPushButton(self.search_tab_frame)
        self.search_button.setMinimumSize(QtCore.QSize(0, 34))
        self.horizontalLayout.addWidget(self.search_button)
        # End Search Controls

        # Result Area
        self.scrollArea = QScrollArea(self.search_tab)
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 781, 312))

        self.result_area_vertical_layout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.search_tab_vertical_layout.addWidget(self.scrollArea)
        # End Result Area

        """        
     ████████ ██████   █████   ██████ ██   ██ ██ ███    ██  ██████  
        ██    ██   ██ ██   ██ ██      ██  ██  ██ ████   ██ ██       
        ██    ██████  ███████ ██      █████   ██ ██ ██  ██ ██   ███ 
        ██    ██   ██ ██   ██ ██      ██  ██  ██ ██  ██ ██ ██    ██ 
        ██    ██   ██ ██   ██  ██████ ██   ██ ██ ██   ████  ██████                                                                                                                             
        """

        self.tracking_tab = QWidget()
        self.tabWidget.addTab(self.tracking_tab, "Tracking")


        """
         ██████  ██████  ████████ ██  ██████  ███    ██ ███████ 
        ██    ██ ██   ██    ██    ██ ██    ██ ████   ██ ██      
        ██    ██ ██████     ██    ██ ██    ██ ██ ██  ██ ███████ 
        ██    ██ ██         ██    ██ ██    ██ ██  ██ ██      ██ 
         ██████  ██         ██    ██  ██████  ██   ████ ███████                                                                                                             
        """

        
        self.console_log = QPlainTextEdit(self.centralwidget)
        self.console_log.setEnabled(True)
        self.console_log.setMaximumSize(QtCore.QSize(16777215, 200))
        self.console_log.setFrameShadow(QFrame.Sunken)
        self.console_log.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.console_log.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.console_log.setReadOnly(True)
        self.console_log.setPlainText("")
        self.console_log.setBackgroundVisible(False)
        self.console_log.setCenterOnScroll(True)
        self.console_log.setPlaceholderText("")
        self.central_vertical_layout.addWidget(self.console_log)
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.central_vertical_layout.addWidget(self.progressBar)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 805, 22))
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

        self.tabWidget.setCurrentIndex(0)



        
        self.search_query_textbox.setPlaceholderText(
            "Enter Product URL or Search Query")
        self.search_button.setText("Search")
        self.menuFile.setTitle("File")
        self.menuSettings.setTitle("Settings")
        self.menuAbout.setTitle("About")
        self.actionQuit.setText("Quit")
        self.actionShow_Logs.setText("Show Logs")

        self.updateConsole("Buyeradar v0.0.1")
        self.updateConsole("")
        self.updateConsole("")

        self.search_button.clicked.connect(self.search_button_clicked)

    def updateConsole(self, message):
        self.CONSOLE_TEXT += message + "\n"
        self.console_log.setPlainText(self.CONSOLE_TEXT)
        self.console_log.moveCursor(QtGui.QTextCursor.End)


import pickle
from func import load_unique_from_database
from components.result_card import ResultCard
from components.track_card import TrackCard
from func import fetch_amazon_html, scrape_html, Product
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

# Default Options
OPTIONS = {
    "debug": False,
    "debug_file": "test.txt",
    "show-images": True,
}


class MainWindow(QMainWindow):

    """
    This function is used to save the options dictionary to a file using pickle.
    """
    def save_options(self):
        with open("options.dat", "wb") as f:
            pickle.dump(OPTIONS, f)
    
    """
    This function is used to load the options dictionary
    form a file using pickle
    """
    def load_options(self):
        try:
            with open("options.dat", "rb") as f:
                global OPTIONS
                OPTIONS = pickle.load(f)
        except:
            """
            If the file does not exist, then default values of 
            options will be applied
            """
            self.updateConsole("No options.dat file found")
        
        # Update controls in the options tab.
        self.debug_checkbox.setChecked(OPTIONS["debug"])
        self.show_product_images_checkbox.setChecked(
            OPTIONS["show-images"])
        self.debugfile_textbox.setText(OPTIONS["debug_file"])
        

    def update_bar(self, value):
        if self.progressBar.value() < 100:
            self.progressBar.setProperty(
                "value", self.progressBar.value()+value)

    def search_button_clicked(self):
        search_query = self.search_query_textbox.toPlainText()

        # Validating search query to be blank or not
        if search_query is None or search_query == "" or search_query.isspace():
            self.updateConsole("Search query cannot be blank")

        else:
            self.updateConsole(f"Search Query set as {search_query}")

            # Remove all exisiting results
            for i in reversed(range(self.result_area_vertical_layout.count())):
                self.result_area_vertical_layout.itemAt(
                    i).widget().setParent(None)

            pg_val = self.progressBar.setProperty
            pg_val('value', 0)
            soup = fetch_amazon_html(
                search_query, self, OPTIONS["debug"], debugfile=OPTIONS["debug_file"])

            # if soup is none, then it means that no results were found
            if soup is None:
                self.updateConsole("No results found")
                return

            # if soup is a Product object
            if isinstance(soup, Product):
                results = [soup]
            else:
                results = scrape_html(soup, self)
                if results is None:
                    pg_val('value', 100)
                    self.updateConsole("No results found")
                    return
            pg_val('value', 100) # Update progressbar value to 100% 


            # Sort the results based on what the user selected from
            # the combolist
            if self.comboBox.currentText() == "Price: Low to High":
                results = sorted(
                    results, key=lambda x: x.price, reverse=False)
            elif self.comboBox.currentText() == "Price: High to Low":
                results = sorted(
                    results, key=lambda x: x.price, reverse=True)

            # Show results
            self.updateConsole("Creating Result Cards")
            QApplication.processEvents()
            i = 0
            for result in results:
                card = ResultCard(result, OPTIONS)
                self.result_area_vertical_layout.addWidget(card)
                i += 1

    def refresh_button_clicked(self):
        tracking = load_unique_from_database()
        # This will return a list of records that have all
        # unique products.

        # Remove all exisiting results
        for i in reversed(range(self.tracking_area_vertical_layout.count())):
            self.tracking_area_vertical_layout.itemAt(
                i).widget().setParent(None)


        # Each record is also in the form of a list, so we can parse
        # the record and get the product object
        if tracking is not None:
            for record in tracking:
                product = Product(
                    id=record[1], name=record[2], price=record[3], image_url=record[5], source=record[4])
                card = TrackCard(product, OPTIONS, self)
                self.tracking_area_vertical_layout.addWidget(card)
        else:
            self.updateConsole("No tracking records found")


    def setupUi(self):

        #Set secondary window as none
        self.a = None

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

        self.result_area_vertical_layout = QVBoxLayout(
            self.scrollAreaWidgetContents)
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

        self.tracking_tab_vertical_layout = QVBoxLayout(self.tracking_tab)
        self.tracking_tab_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.tracking_tab_vertical_layout.setSpacing(0)

        self.tracking_tab_frame = QFrame(self.tracking_tab)
        self.tracking_tab_frame.setMaximumSize(QtCore.QSize(16777215, 75))
        self.tracking_tab_frame.setFrameShape(QFrame.StyledPanel)
        self.tracking_tab_frame.setFrameShadow(QFrame.Raised)
        self.tracking_tab_vertical_layout.addWidget(self.tracking_tab_frame)

        # A button with the title "refresh"
        self.refresh_button = QPushButton(self.tracking_tab_frame)
        self.refresh_button.setMinimumSize(QtCore.QSize(0, 34))
        self.refresh_button.setMaximumSize(QtCore.QSize(16777215, 34))
        self.refresh_button.setText("Refresh")
        self.tracking_tab_vertical_layout.addWidget(self.refresh_button)
        # On clicking refresh button, refresh_button_clicked function will be called
        self.refresh_button.clicked.connect(self.refresh_button_clicked)

        # Scrollable view for tracking products
        self.scrollArea_2 = QScrollArea(self.tracking_tab)
        self.scrollArea_2.setWidgetResizable(True)

        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(
            QtCore.QRect(0, 0, 781, 312))

        self.tracking_area_vertical_layout = QVBoxLayout(
            self.scrollAreaWidgetContents_2)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.tracking_tab_vertical_layout.addWidget(self.scrollArea_2)
        # End Scrollable view for tracking products

        """
         ██████  ██████  ████████ ██  ██████  ███    ██ ███████
        ██    ██ ██   ██    ██    ██ ██    ██ ████   ██ ██
        ██    ██ ██████     ██    ██ ██    ██ ██ ██  ██ ███████
        ██    ██ ██         ██    ██ ██    ██ ██  ██ ██      ██
         ██████  ██         ██    ██  ██████  ██   ████ ███████
        """

        self.options_tab = QWidget()
        self.tabWidget.addTab(self.options_tab, "Options")

        self.options_tab_vertical_layout = QVBoxLayout(self.options_tab)
        self.options_tab_vertical_layout.setContentsMargins(20, 20, 20, 20)
        self.options_tab_vertical_layout.setSpacing(0)

        # Create a checkbox with text "Debug" and add it to vertitcal layout of options tab
        self.debug_checkbox = QCheckBox(self.options_tab)
        self.debug_checkbox.setText("Debug")
        self.options_tab_vertical_layout.addWidget(self.debug_checkbox)

        # If debug_checkbox is checked then set debug to True else set debug to False
        self.debug_checkbox.stateChanged.connect(
            lambda: self.set_debug(self.debug_checkbox.isChecked()))

        # Create a horizontal layout called "debugfile_layout" and add it to
        # vertical layout of options tab
        self.debugfile_layout = QHBoxLayout()
        self.options_tab_vertical_layout.addLayout(self.debugfile_layout)
        self.debugfile_layout.setSpacing(10)

        # Create a label called "debugfilelabel" with text as "Debug File: "
        # and add it to debugfile_layout
        self.debugfilelabel = QLabel(self.options_tab)
        self.debugfilelabel.setText("Debug File: ")
        self.debugfile_layout.addWidget(self.debugfilelabel)

        # Create a textbox "debugfile_textbox"
        self.debugfile_textbox = QLineEdit(self.options_tab)
        self.debugfile_textbox.setText("test.txt")
        self.debugfile_layout.addWidget(self.debugfile_textbox)

        # Create a checkbox "Show product images" and add it to vertical layout of options tab
        self.show_product_images_checkbox = QCheckBox(self.options_tab)
        self.show_product_images_checkbox.setText("Show product images")
        self.options_tab_vertical_layout.addWidget(
            self.show_product_images_checkbox)

        # If show_product_images_checkbox is checked then set show_product_images to True else set show_product_images to False
        self.show_product_images_checkbox.stateChanged.connect(
            lambda: self.set_show_product_images(self.show_product_images_checkbox.isChecked()))

        # Creating a console_log widget
        self.console_log = QPlainTextEdit(self.centralwidget)
        self.console_log.setEnabled(True)
        self.console_log.setMaximumSize(QtCore.QSize(16777215, 200))
        self.console_log.setFrameShadow(QFrame.Sunken)
        self.console_log.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)
        self.console_log.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents)
        self.console_log.setReadOnly(True)
        self.console_log.setPlainText("")
        self.console_log.setBackgroundVisible(False)
        self.console_log.setCenterOnScroll(True)
        self.console_log.setPlaceholderText("")
        self.central_vertical_layout.addWidget(self.console_log)

        # Creating a progressbar widget
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.central_vertical_layout.addWidget(self.progressBar)
        self.setCentralWidget(self.centralwidget)

        # Creating a menubar
        self.menupdate_bar = QMenuBar(self)
        self.menupdate_bar.setGeometry(QtCore.QRect(0, 0, 805, 22))
        self.menuFile = QMenu(self.menupdate_bar)
        self.menuSettings = QMenu(self.menupdate_bar)
        self.menuAbout = QMenu(self.menupdate_bar)
        self.setMenuBar(self.menupdate_bar)
        self.actionQuit = QAction(self)
        self.actionShow_Logs = QAction(self)
        self.actionShow_Logs.setCheckable(True)
        self.menuFile.addAction(self.actionQuit)
        self.menuSettings.addAction(self.actionShow_Logs)
        self.menupdate_bar.addAction(self.menuFile.menuAction())
        self.menupdate_bar.addAction(self.menuSettings.menuAction())
        self.menupdate_bar.addAction(self.menuAbout.menuAction())

        # Creating a statusbar
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

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

    def set_debug(self, debug):
        global OPTIONS
        OPTIONS["debug"] = debug
        self.updateConsole("Debug set to " + str(OPTIONS["debug"]))

    def set_show_product_images(self, show_product_images):
        global OPTIONS
        OPTIONS["show_product_images"] = show_product_images
        self.updateConsole("Show product images set to " + \
                           str(OPTIONS["show_product_images"]))

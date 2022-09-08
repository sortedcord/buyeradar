
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from func import trim_name
import requests

class ProductWindow(QMainWindow):
    def __init__(self, product, OPTIONS):
        super().__init__()
        self.setupUi(product, OPTIONS)

    def setupUi(self, product, OPTIONS):
        self.resize(963, 600)
        self.centralwidget = QWidget(self)

        self.horizontalLayout = QHBoxLayout(self.centralwidget)

        self.buttonBox = QDialogButtonBox(self.centralwidget)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Discard|QDialogButtonBox.Ok|QDialogButtonBox.Reset)
        # self.buttonBox.accepted.connect(self.accept) # type: ignore
        #self.buttonBox.rejected.connect(self.reject) # type: ignore
        self.horizontalLayout.addWidget(self.buttonBox)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setFrameShadow(QFrame.Plain)
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 839, 525))

        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)

        self.product_title = QLabel(self.scrollAreaWidgetContents)        
        font = QtGui.QFont()
        font.setPointSize(24)
        self.product_title.setFont(font)
        self.verticalLayout.addWidget(self.product_title)

        self.product_image = QLabel(self.scrollAreaWidgetContents)
        self.product_image.setMinimumSize(QtCore.QSize(300, 100))
        self.product_image.setMaximumSize(QtCore.QSize(700, 200))
        self.product_image.setText("")
        if not OPTIONS['show-images']:
            self.product_image.hide()
        else:
            self.image = QtGui.QImage()
        try:
            self.image.loadFromData(requests.get(product.image_url).content)
        except:
            print("Could not load image")
        self.product_image.setPixmap(QtGui.QPixmap(self.image))
        self.verticalLayout.addWidget(self.product_image)

        self.tableView = QTableView(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.tableView)

        self.current_price_label = QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.current_price_label.setFont(font)
        self.verticalLayout.addWidget(self.current_price_label)

        self.price_analytics_label = QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.price_analytics_label.setFont(font)
        self.verticalLayout.addWidget(self.price_analytics_label)

        self.frame = QFrame(self.scrollAreaWidgetContents)
        self.frame.setMinimumSize(QtCore.QSize(0, 0))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Plain)
        self.verticalLayout.addWidget(self.frame)

        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.fetch_data_button = QPushButton(self.frame)
        self.horizontalLayout_2.addWidget(self.fetch_data_button)

        self.progressBar = QProgressBar(self.frame)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setInvertedAppearance(False)
        self.horizontalLayout_2.addWidget(self.progressBar)
        
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.setCentralWidget(self.centralwidget)

        self.setWindowTitle("Product Window")
        self.product_title.setText(trim_name(product.name))
        self.current_price_label.setText(str(product.price))
        self.price_analytics_label.setText("Min: Max: Average:")
        self.fetch_data_button.setText("Update Prices")

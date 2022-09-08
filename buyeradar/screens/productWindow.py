
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from func import trim_name, load_single_product, fetch_amazon_page_content, save_to_database
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
        self.buttonBox.setStandardButtons(QDialogButtonBox.Discard|QDialogButtonBox.Ok)
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

        try:
            table = load_single_product(product.id)
        except:
            print("Could not load table")
        else:
            prices = []
            for row in table:
                prices.append(row[3])

            # Get average value of all elements in prices list
            avg = sum(prices) / len(prices)

            # Get the minimum value of all elements in prices list
            min_price = min(prices)

            # Get the maximum value of all elements in prices list
            max_price = max(prices)

            headers = ["Record ID", "Source", "Price", "Date Time", "Deviation"]
            self.tableWidget = QTableWidget(self.scrollAreaWidgetContents)
            self.tableWidget.setColumnCount(len(headers))
            self.tableWidget.setRowCount(len(table))
            for header in headers:
                item = QtWidgets.QTableWidgetItem()
                item.setText(header)
                self.tableWidget.setHorizontalHeaderItem(headers.index(header), item)
            
            self.tableWidget.setColumnWidth(3, 250)
            x=0
            for row in table:
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(table.index(row)))
                self.tableWidget.setVerticalHeaderItem(table.index(row), item)

                recordid = row[0]
                pprice= row[3]
                psource = row[4]
                pdate = row[6]

                # get percentage change in current price from avg
                deviation = float(((pprice - avg) / avg) * 100)
                # round it off to 2 decimal places
                deviation = round(deviation, 2)

                row_ = (str(recordid), psource, str(pprice), pdate, str(deviation)+"%")

                y=0
                for column in row_:
                    self.tableWidget.setItem(x, y, QTableWidgetItem(str(column)))
                    y+=1
                x+=1
            self.verticalLayout.addWidget(self.tableWidget)

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
        self.price_analytics_label.setText(f"Min: {min_price} Max: {max_price} Average: {avg}")
        self.fetch_data_button.setText("Update Prices")

        self.fetch_data_button.clicked.connect(lambda: self.fetch_data_button_clicked(product))
    
    def fetch_data_button_clicked(self, product):
        self.fetch_data_button.setDisabled(True)
        self.fetch_data_button.setText("Fetching Data...")
        self.progressBar.setValue(0)

        product = fetch_amazon_page_content(f"https://www.amazon.in/dp/{product.id}")

        self.progressBar.setValue(50)

        save_to_database(product)

        self.progressBar.setValue(100)
        self.fetch_data_button.setText("Update Prices")
        self.fetch_data_button.setDisabled(False)

        self.progressBar.setValue(0)

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
import requests
from func import load_single_product
from screens.productWindow import ProductWindow

from func import trim_name


class TrackCard(QWidget):
    def __init__(self, product, OPTIONS, mainwindow):
        super().__init__()
        self.setupUi(product, OPTIONS, mainwindow)

    def setupUi(self, product, OPTIONS, mainwindow):
        self.resize(720, 218)
        self.horizontalLayout = QHBoxLayout(self)

        self.picture = QLabel(self)
        self.picture.setMinimumSize(QtCore.QSize(128, 128))
        self.picture.setMaximumSize(QtCore.QSize(175, 200))
        self.picture.setText("")
        self.image = QtGui.QImage()
        try:
            self.image.loadFromData(requests.get(product.image_url).content)
        except:
            print("Could not load image")
        self.picture.setPixmap(QtGui.QPixmap(self.image))
        self.horizontalLayout.addWidget(self.picture)

        self.main_frame = QFrame(self)
        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.main_frame)

        self.product_name_label = QLabel(self.main_frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.product_name_label.setFont(font)
        self.verticalLayout_2.addWidget(self.product_name_label)
        self.product_source_label = QLabel(self.main_frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.product_source_label.setFont(font)
        self.verticalLayout_2.addWidget(self.product_source_label)
        self.product_id = QLabel(self.main_frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.product_id.setFont(font)
        self.product_id.setStyleSheet("color: rgb(202, 202, 202);")
        self.verticalLayout_2.addWidget(self.product_id)
        spacerItem = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.product_price_label = QLabel(self.main_frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.product_price_label.setFont(font)
        self.verticalLayout_2.addWidget(self.product_price_label)
        self.product_price_cal_label = QLabel(self.main_frame)
        self.verticalLayout_2.addWidget(self.product_price_cal_label)
        self.view_more_button = QPushButton(self.main_frame)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.view_more_button.sizePolicy().hasHeightForWidth())
        self.view_more_button.setSizePolicy(sizePolicy)
        self.view_more_button.setMinimumSize(QtCore.QSize(125, 35))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.view_more_button.setFont(font)
        self.verticalLayout_2.addWidget(self.view_more_button)
        self.horizontalLayout.addWidget(self.main_frame)

        self.product_name_label.setText(trim_name(product.name))
        self.product_source_label.setText(f"Fetched from {product.source}")
        self.product_id.setText(f"ID: {product.id}")
        self.product_price_label.setText(f"CURRENTLY: INR {product.price}")

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
            # round to 2 decimal places
            avg = round(avg, 2)

            # Get the minimum value of all elements in prices list
            min_price = min(prices)

            # Get the maximum value of all elements in prices list
            max_price = max(prices)

        self.product_price_cal_label.setText(
            f"Max: {max_price} Min: {min_price} Avg: {avg}")
        self.view_more_button.setText("View")

        self.view_more_button.clicked.connect(
            lambda: self.view_more_button_clicked(product, OPTIONS, mainwindow))

    def view_more_button_clicked(self, product, OPTIONS, mainwindow):
        print("View more button clicked")

        mainwindow.a = ProductWindow(product, OPTIONS)
        mainwindow.a.show()

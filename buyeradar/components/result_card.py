import time
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from func import save_to_database
import requests
from func import trim_name


class ResultCard(QWidget):
    def __init__(self, product, OPTIONS):
        super().__init__()
        self.showUI(product, OPTIONS)
        self.setConnections(product)

    def showUI(self, product, OPTIONS):
        # Set the size of the card
        self.resize(724, 200)
        self.setMinimumSize(QtCore.QSize(724, 200))
        self.setMaximumSize(QtCore.QSize(16777215, 253))

        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel(self)
        self.image_label.setMinimumSize(QtCore.QSize(128, 128))
        self.image_label.setMaximumSize(QtCore.QSize(175, 200))
        self.horizontalLayout.addWidget(self.image_label)

        self.main_frame = QFrame(self)
        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout.addWidget(self.main_frame)

        self.verticalLayout = QVBoxLayout(self.main_frame)

        self.product_title = QLabel(self.main_frame)
        self.product_title.setText(trim_name(product.name))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.product_title.setFont(font)
        self.verticalLayout.addWidget(self.product_title)

        self.source_label = QLabel(self.main_frame)
        self.source_label.setText("Fetched from Amazon.com")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.source_label.setFont(font)
        self.verticalLayout.addWidget(self.source_label)

        self.id_label = QLabel(self.main_frame)
        self.id_label.setText(f"ID: {product.id}")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.id_label.setFont(font)
        self.id_label.setStyleSheet("color: rgb(202, 202, 202);")
        self.verticalLayout.addWidget(self.id_label)

        # Gives spacing between items
        spacerItem = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.price_label = QLabel(self.main_frame)
        self.price_label.setText(f"INR {product.price}")
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.price_label.setFont(font)
        self.verticalLayout.addWidget(self.price_label)

        self.track_button = QPushButton(self.main_frame)
        self.track_button.setText("Track")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.track_button.sizePolicy().hasHeightForWidth())
        self.track_button.setSizePolicy(sizePolicy)
        self.track_button.setMinimumSize(QtCore.QSize(125, 35))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.track_button.setFont(font)
        self.verticalLayout.addWidget(self.track_button)

        # Set the image if options does not have it disabled
        if  OPTIONS["show-images"]:
            self.image = QtGui.QImage()
            try:
                self.image.loadFromData(requests.get(product.image_url).content)
            except:
                print("Could not load image")
            self.image_label.setPixmap(QtGui.QPixmap(self.image))

    def setConnections(self, product):
        # When the track button is clicked save to dabase with product
        self.track_button.clicked.connect(
            lambda: self.track_button_clicked(product))

    def track_button_clicked(self, product):
        print("Track button clicked")
        save_to_database(product)
        self.track_button.setText("Tracking")
        # Disable the button
        self.track_button.setEnabled(False)

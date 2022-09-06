from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
import requests


from func import trim_name


class ResultCard(QWidget):
    def __init__(self, product):
        super().__init__()
        self.showUI(product)

    def showUI(self, product):
        self.resize(724, 200)
        self.setMinimumSize(QtCore.QSize(724, 200))
        self.setMaximumSize(QtCore.QSize(16777215, 253))
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self)
        self.label_3.setMinimumSize(QtCore.QSize(128, 128))
        self.label_3.setMaximumSize(QtCore.QSize(175, 200))
        self.horizontalLayout.addWidget(self.label_3)
        self.main_frame = QFrame(self)
        self.main_frame.setStyleSheet("")
        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.main_frame)
        self.product_title = QLabel(self.main_frame)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.product_title.sizePolicy().hasHeightForWidth())
        self.product_title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.product_title.setFont(font)
        self.verticalLayout.addWidget(self.product_title)
        self.source_label = QLabel(self.main_frame)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.source_label.sizePolicy().hasHeightForWidth())
        self.source_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.source_label.setFont(font)
        self.verticalLayout.addWidget(self.source_label)
        self.label = QLabel(self.main_frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(202, 202, 202);")
        self.verticalLayout.addWidget(self.label)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_2 = QLabel(self.main_frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.verticalLayout.addWidget(self.label_2)
        self.track_button = QPushButton(self.main_frame)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.track_button.sizePolicy().hasHeightForWidth())
        self.track_button.setSizePolicy(sizePolicy)
        self.track_button.setMinimumSize(QtCore.QSize(125, 35))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.track_button.setFont(font)
        self.verticalLayout.addWidget(self.track_button)
        self.horizontalLayout.addWidget(self.main_frame)

        self.product_title.setText(trim_name(product.name))
        self.source_label.setText("Fetched from Amazon.com")
        self.label.setText(f"ID: {product.id}")
        self.label_2.setText(f"INR {product.price}")
        self.track_button.setText("Track")

        self.image = QtGui.QImage()
        try:
            self.image.loadFromData(requests.get(product.image_url).content)
        except:
            print("Could not load image")
        self.label_3.setPixmap(QtGui.QPixmap(self.image))
    
    def setConnections(self, product):
        # When the track button is clicked save to dabase with product
        self.track_button.clicked.connect(lambda: self.save_to_database(product))

    def save_to_database(self, product):
        import random
            

        id = product.id
        name = product.name
        price = product.price

        # Code here to save to
        # database

        import sqlite3

        conn=sqlite3.connect('project.db')
        cursor=conn.cursor()

        recordid=random.randint(10000,99999)
        pid=id
        pname=name
        pprice=float(int(price))
        psource="Amazon"

        command = "insert into product values('{}','{}','{}','{}','{}');".format(recordid,pid,pname,pprice,psource)


        cursor.execute(command)
        conn.commit()
        print("Saved in database")
        cursor.close()












































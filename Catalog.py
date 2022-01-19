import sqlite3
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView

from Book import Book


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(1280, 720)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 200, 1240, 500))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        delegate = ReadOnlyDelegate(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(0, delegate)
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        self.font = QtGui.QFont()
        self.font.setFamily("Agency FB")
        self.font.setPointSize(72)
        self.font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(660, 20, 600, 160))
        self.pushButton.setFont(self.font)
        self.pushButton.setObjectName("pushButton")
        self.font.setPointSize(28)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(20, 20, 620, 70))
        self.comboBox.setFont(self.font)
        self.comboBox.addItem("Название")
        self.comboBox.addItem("Автор")
        self.comboBox.setObjectName("comboBox")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(20, 110, 620, 70))
        self.lineEdit.setFont(self.font)
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Поиск"))


class Catalog(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logic()

    def logic(self):
        self.pushButton.clicked.connect(self.search)

    def search(self):
        t = self.lineEdit.text()
        v = self.comboBox.currentText()
        if not t:
            return
        con = sqlite3.connect("LibraryOfBooks.db")
        cur = con.cursor()
        if v == "Автор":
            books = cur.execute(f'''
                    SELECT
                        Books.title
                    FROM
                        Books    
                    WHERE
                        Books.authorId = (
                                        SELECT
                                            Authors.id
                                        FROM
                                            Authors
                                        WHERE  
                                            Authors.name LIKE '%{t}%')''').fetchall()
        else:
            books = cur.execute(f'''
                    SELECT
                        Books.title
                    FROM
                        Books
                    WHERE
                        Books.title LIKE "%{t}%"''').fetchall()
        self.tableWidget.setRowCount(0)
        for col, i in enumerate(books):
            btn = QtWidgets.QPushButton()
            btn.setText(*i)
            self.font.setPointSize(16)
            btn.setFont(self.font)
            btn.clicked.connect(self.book)
            self.tableWidget.setRowCount(col + 1)
            self.tableWidget.setCellWidget(col, 0, btn)

    def book(self):
        self.w = Book(self.sender().text())
        self.w.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Catalog()
    ex.show()
    sys.exit(app.exec())

import sqlite3

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(480, 720)
        self.font = QtGui.QFont()
        self.font.setFamily("Agency FB")
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.picture = QtWidgets.QLabel(Dialog)
        self.picture.setGeometry(QtCore.QRect(115, 20, 250, 300))
        self.picture.setAlignment(QtCore.Qt.AlignCenter)
        self.picture.setObjectName("picture")
        self.labelTitle = QtWidgets.QLabel(Dialog)
        self.labelTitle.setGeometry(QtCore.QRect(20, 340, 440, 40))
        self.labelTitle.setFont(self.font)
        self.labelTitle.setText("Название")
        self.labelTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitle.setObjectName("labelTitle")
        self.labelAuthor = QtWidgets.QLabel(Dialog)
        self.labelAuthor.setGeometry(QtCore.QRect(20, 435, 440, 40))
        self.labelAuthor.setFont(self.font)
        self.labelAuthor.setText("Автор")
        self.labelAuthor.setAlignment(QtCore.Qt.AlignCenter)
        self.labelAuthor.setObjectName("labelAuthor")
        self.labelYear = QtWidgets.QLabel(Dialog)
        self.labelYear.setGeometry(QtCore.QRect(20, 530, 440, 40))
        self.labelYear.setFont(self.font)
        self.labelYear.setText("Год выпуска")
        self.labelYear.setAlignment(QtCore.Qt.AlignCenter)
        self.labelYear.setObjectName("labelYear")
        self.labelGenre = QtWidgets.QLabel(Dialog)
        self.labelGenre.setGeometry(QtCore.QRect(20, 625, 440, 40))
        self.labelGenre.setFont(self.font)
        self.labelGenre.setText("Жанр")
        self.labelGenre.setAlignment(QtCore.Qt.AlignCenter)
        self.labelGenre.setObjectName("labelGenre")

        self.font.setPointSize(14)
        self.font.setBold(False)
        self.labelGenre2 = QtWidgets.QLabel(Dialog)
        self.labelGenre2.setGeometry(QtCore.QRect(20, 675, 440, 25))
        self.labelGenre2.setFont(self.font)
        self.labelGenre2.setAlignment(QtCore.Qt.AlignCenter)
        self.labelGenre2.setObjectName("labelGenre2")
        self.labelYear2 = QtWidgets.QLabel(Dialog)
        self.labelYear2.setGeometry(QtCore.QRect(20, 580, 440, 25))
        self.labelYear2.setFont(self.font)
        self.labelYear2.setAlignment(QtCore.Qt.AlignCenter)
        self.labelYear2.setObjectName("labelYear2")
        self.labelTitle2 = QtWidgets.QLabel(Dialog)
        self.labelTitle2.setGeometry(QtCore.QRect(20, 390, 440, 25))
        self.labelTitle2.setFont(self.font)
        self.labelTitle2.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitle2.setObjectName("labelTitle2")
        self.labelAuthor2 = QtWidgets.QLabel(Dialog)
        self.labelAuthor2.setGeometry(QtCore.QRect(20, 485, 440, 25))
        self.labelAuthor2.setFont(self.font)
        self.labelAuthor2.setAlignment(QtCore.Qt.AlignCenter)
        self.labelAuthor2.setObjectName("labelAuthor2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


class Book(QMainWindow, Ui_Dialog):
    def __init__(self, name):
        super().__init__()
        self.setupUi(self)
        self.name = name
        self.logic()

    def logic(self):
        con = sqlite3.connect("LibraryOfBooks.db")
        cur = con.cursor()
        BDB = cur.execute(f'''
                           SELECT
                               title,
                               year,
                               picture
                            FROM
                               Books
                            WHERE
                                Books.title = "{self.name}"''').fetchall()
        BDB = list(BDB[0])
        pixmap = QtGui.QPixmap(BDB[2]).scaled(250, 300, Qt.KeepAspectRatio)
        self.picture.setPixmap(pixmap)
        self.labelTitle2.setText(BDB[0])
        self.labelYear2.setText(str(BDB[1]))

        GDB = cur.execute(f'''
                            SELECT
                               title
                            FROM
                               Genres
                            WHERE
                                id = (
                                    SELECT
                                        genreId
                                    FROM
                                        Books
                                    WHERE
                                        title = "{self.name}")''').fetchall()
        GDB = list(GDB[0])
        self.labelGenre2.setText(GDB[0])

        ADB = cur.execute(f'''
                            SELECT
                               name
                            FROM
                               Authors
                            WHERE
                                id = (
                                    SELECT
                                        authorId
                                    FROM
                                        Books
                                    WHERE
                                        title = "{self.name}")''').fetchall()
        ADB = list(ADB[0])
        self.labelAuthor2.setText(ADB[0])

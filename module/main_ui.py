# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QMenuBar, QPlainTextEdit, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(940, 596)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.input_code = QPlainTextEdit(self.centralwidget)
        self.input_code.setObjectName(u"input_code")
        self.input_code.setGeometry(QRect(10, 30, 481, 371))
        self.input_code.setCursorWidth(1)
        self.button_compile = QPushButton(self.centralwidget)
        self.button_compile.setObjectName(u"button_compile")
        self.button_compile.setGeometry(QRect(10, 420, 75, 24))
        self.output_messages = QPlainTextEdit(self.centralwidget)
        self.output_messages.setObjectName(u"output_messages")
        self.output_messages.setEnabled(True)
        self.output_messages.setGeometry(QRect(10, 480, 921, 81))
        self.output_messages.setReadOnly(True)
        self.output_messages.setCursorWidth(0)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 457, 101, 16))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 10, 101, 16))
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(500, 10, 431, 391))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.output_table_result = QTableWidget(self.tab)
        self.output_table_result.setObjectName(u"output_table_result")
        self.output_table_result.setGeometry(QRect(0, 0, 421, 361))
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.output_sintax_analyzer = QPlainTextEdit(self.tab_2)
        self.output_sintax_analyzer.setObjectName(u"output_sintax_analyzer")
        self.output_sintax_analyzer.setGeometry(QRect(0, 0, 421, 361))
        self.output_sintax_analyzer.setCursorWidth(1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.output_semantic_analyzer = QPlainTextEdit(self.tab_3)
        self.output_semantic_analyzer.setObjectName(u"output_semantic_analyzer")
        self.output_semantic_analyzer.setGeometry(QRect(0, 0, 421, 361))
        self.output_semantic_analyzer.setCursorWidth(1)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.output_assembly_code = QPlainTextEdit(self.tab_4)
        self.output_assembly_code.setObjectName(u"output_assembly_code")
        self.output_assembly_code.setGeometry(QRect(0, 0, 421, 361))
        self.output_assembly_code.setCursorWidth(1)
        self.tabWidget.addTab(self.tab_4, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 940, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.button_compile.setText(QCoreApplication.translate("MainWindow", u"Analizar", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Mensajes (Logs)", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Editor", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Analisis Lexico", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Analisis Sint\u00e1ctico", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Analisis Sem\u00e1ntico", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"ENSAM", None))
    # retranslateUi


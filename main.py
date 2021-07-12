from os import name, stat
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp, QSize, fixed, pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QBoxLayout, QColorDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLayout, QPushButton, QScrollArea, QSpacerItem, QTabWidget, QVBoxLayout, QWIDGETSIZE_MAX, QWidget, QInputDialog, QLineEdit, QFileDialog, QMdiSubWindow
from matplotlib import scale
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.colors import cnames
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.core.accessor import PandasDelegate
import sys

import stats
import rannum

class Ui_Main(QWidget):

    def __init__(self):
        super(Ui_Main, self).__init__()
        self.secondWindow = None

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Tecnicas de simulación")
        MainWindow.resize(813, 700)

        self.centralwidget = QtWidgets.QWidget(MainWindow)

        btnSize = QSize(100, 50)

        self.statsButton = QPushButton('Estadística', self.centralwidget)
        self.statsButton.setMaximumSize(btnSize)
        self.statsButton.clicked.connect(lambda: self.openStats())

        self.randButton = QPushButton('Aleatorios', self.centralwidget)
        self.randButton.setMaximumSize(btnSize)
        self.randButton.clicked.connect(lambda: self.openRand())

        self.layout = QHBoxLayout(self.centralwidget)
        self.layout.addWidget(self.statsButton)
        self.layout.addWidget(self.randButton)
        #self.layout.addStretch()

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def openStats(self):
        self.secondWindow = stats.Ui_Stats()
        self.secondWindow.show()

    def openRand(self):
        self.secondWindow = rannum.RandNum()
        self.secondWindow.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Main()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QPushButton, QWidget
import sys

import stats as sts
import rannum as rn
import forecasting as fcstng
import simulations as sims

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

        self.forecastButton = QPushButton('Pronosticos', self.centralwidget)
        self.forecastButton.setMaximumSize(btnSize)
        self.forecastButton.clicked.connect(lambda: self.openForecasting())

        self.simulationButton = QPushButton('Simulación', self.centralwidget)
        self.simulationButton.setMaximumSize(btnSize)
        self.simulationButton.clicked.connect(lambda: self.openSimulation())

        self.layout = QHBoxLayout(self.centralwidget)
        self.layout.addWidget(self.statsButton)
        self.layout.addWidget(self.randButton)
        self.layout.addWidget(self.forecastButton)
        self.layout.addWidget(self.simulationButton)

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def openStats(self):

        self.hide
        self.secondWindow = sts.Ui_Stats()
        self.secondWindow.show()

    def openRand(self):

        self.secondWindow = rn.RandNum()
        self.secondWindow.show()

    def openForecasting(self):

        self.secondWindow = fcstng.Forecasting()
        self.secondWindow.show()

    def openSimulation(self):

        self.secondWindow = sims.Simulation()
        self.secondWindow.show()

if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Main()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
from os import name
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp, fixed, pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QBoxLayout, QColorDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLayout, QMainWindow, QPushButton, QScrollArea, QSpacerItem, QVBoxLayout, QWIDGETSIZE_MAX, QWidget, QInputDialog, QLineEdit, QFileDialog, QMdiSubWindow
from matplotlib import scale
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.colors import cnames
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.core.accessor import PandasDelegate

import dfModel

mod = dfModel.DataFrameModel

class Ui_Stats(QMainWindow):
    datos = ""
    conjuntoDatos = ""

    def __init__(self):
        super(Ui_Stats, self).__init__()
        global conjuntoDatos 
        conjuntoDatos = []
        self.resize(813, 700)

        self.colorDialog = QColorDialog(self)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.labelSelect = QtWidgets.QLabel(self.centralwidget)
        self.labelSelect.setGeometry(QtCore.QRect(10, 0, 171, 39))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSelect.sizePolicy().hasHeightForWidth())
        self.labelSelect.setSizePolicy(sizePolicy)
        self.labelSelect.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.labelSelect.setFont(font)
        self.labelSelect.setObjectName("labelSelect")
        self.selectFileBtn = QtWidgets.QToolButton(self.centralwidget)
        self.selectFileBtn.setGeometry(QtCore.QRect(180, 10, 25, 19))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectFileBtn.sizePolicy().hasHeightForWidth())
        self.selectFileBtn.setSizePolicy(sizePolicy)
        self.selectFileBtn.setMaximumSize(QtCore.QSize(25, 16777215))
        self.selectFileBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.selectFileBtn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.selectFileBtn.setObjectName("selectFileBtn")
        self.selectFileBtn.clicked.connect(lambda: self.openFileNameDialog())
        self.lineFileName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineFileName.setGeometry(QtCore.QRect(210, 10, 171, 21))
        self.lineFileName.setReadOnly(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineFileName.sizePolicy().hasHeightForWidth())
        self.lineFileName.setSizePolicy(sizePolicy)
        self.lineFileName.setMaximumSize(QtCore.QSize(500, 16777215))
        self.lineFileName.setFont(font)
        self.lineFileName.setObjectName("lineFileName")
        self.graphicBtn = QtWidgets.QPushButton(self.centralwidget)
        self.graphicBtn.setGeometry(QtCore.QRect(390, 10, 100, 23))
        self.graphicBtn.clicked.connect(lambda: self.generateTable())
        self.graphicBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.graphicBtn.setFont(font)
        self.graphicBtn.setObjectName("graphicBtn")
        self.newBtn = QtWidgets.QPushButton(self.centralwidget)
        self.newBtn.setGeometry(QtCore.QRect(495, 10, 100, 23))
        self.newBtn.clicked.connect(lambda: self.clearLayout())
        self.newBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.newBtn.setFont(font)
        self.newBtn.setObjectName("newBtn")
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 813, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.outerGroupBox = QGroupBox(self.centralwidget)
        self.outerGroupBox.setGeometry(0, 40, 795, 640)
        self.horizontalGroupBox = QGroupBox(self.outerGroupBox)
        self.horizontalGroupBox.setGeometry(0, 0, 700, 500)
        scrollArea = QScrollArea()
        scrollArea.setWidget(self.horizontalGroupBox)
        scrollArea.setMinimumSize(500, 50)
        scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scrollArea.setWidgetResizable(True)
        self.outlayout = QVBoxLayout()
        self.outlayout.addWidget(scrollArea)
        self.outerGroupBox.setLayout(self.outlayout)
        self.layout = QVBoxLayout()
        self.horizontalGroupBox.setLayout(self.layout)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    #def setupUi(self, MainWindow):
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Estadistica", "Estadistica"))
        self.labelSelect.setText(_translate("Select a document", "Seleccione un documento"))
        self.selectFileBtn.setText(_translate("...", "..."))
        self.graphicBtn.setText(_translate("Show data", "Mostrar datos"))
        self.newBtn.setText(_translate("New", "Nuevo"))

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.lineFileName.setText(fileName)

    def generateTable(self):
        global datos
        datos = pd.read_csv(self.lineFileName.text())

        model = mod(datos)
        table = QtWidgets.QTableView(parent=self)
        table.setMinimumSize(750, 200)
        table.setMaximumSize(750, 200)
        table.setModel(model)

        labelData = QtWidgets.QLabel()
        labelData.setText("Dato a mostrar")
        labelData.setFont(QtGui.QFont("Calibri", 10))
        lineData = QtWidgets.QLineEdit()
        lineData.setMaximumSize(100, 21)
        lineData.setFont(QtGui.QFont("Calibri", 10))

        labelClasses = QtWidgets.QLabel()
        labelClasses.setText("Cantidad de clases del histograma")
        labelClasses.setFont(QtGui.QFont("Calibri", 10))
        lineClasses = QtWidgets.QLineEdit()
        lineClasses.setMaximumSize(100, 21)
        lineClasses.setFont(QtGui.QFont("Calibri", 10))

        colorBtn = QPushButton()
        colorBtn.setText("Seleccionar color")
        colorBtn.setFont(QtGui.QFont("Calibri", 10))
        colorBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        colorBtn.clicked.connect(lambda: self.selectColor())

        plotBtn = QPushButton()
        plotBtn.setText("Mostrar resultados")
        plotBtn.setFont(QtGui.QFont("Calibri", 10))
        plotBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        plotBtn.clicked.connect(lambda: self.calcular(lineData.text(), int(lineClasses.text())))

        hElement = QWidget()
        hLayout = QHBoxLayout()
        hLayout.addWidget(labelData)
        hLayout.addWidget(lineData)
        hLayout.addWidget(labelClasses)
        hLayout.addWidget(lineClasses)
        hLayout.addWidget(colorBtn)
        hLayout.addWidget(plotBtn)
        hElement.setLayout(hLayout)

        self.layout.addWidget(table)
        self.layout.addWidget(hElement)
        self.layout.addStretch()

    def selectColor(self):
        self.colorDialog.exec_()

    def calcular(self, dataTxt, classQuant):
        global conjuntoDatos

        x = datos[dataTxt]
        color = self.colorDialog.selectedColor().name()
        figure = plt.figure(figsize=(2,2))
        plt.hist(x,bins=classQuant,color=color)
        plt.axvline(x.mean(),color='red',label='Media')
        plt.axvline(x.median(),color='yellow',label='Mediana')
        plt.axvline(x.mode()[0],color='green',label='Moda')
        plt.xlabel('Casos')
        plt.ylabel('Frecuencia')

        conjuntoDatos.append(x)
        
        labelMean = QLabel('Media = ' + str(x.mean()))
        labelMedian = QLabel('Mediana = ' + str(x.median()))
        labelMode = QLabel('Moda = ' + str(x.mode()[0]))

        element = QWidget()
        vLayout = QVBoxLayout()
        vLayout.addWidget(labelMean)
        vLayout.addWidget(labelMedian)
        vLayout.addWidget(labelMode)
        element.setLayout(vLayout)

        canvas = FigureCanvasQTAgg(figure)
        toolbar = NavigationToolbar2QT(canvas, self)
        canvLayout = QVBoxLayout()
        canvLayout.addWidget(toolbar)
        canvLayout.addWidget(canvas)
        canvasElmt = QWidget()
        canvasElmt.setLayout(canvLayout)
        canvasElmt.setMinimumSize(300, 480) 

        labelX = QtWidgets.QLabel()
        labelX.setText("Eje X: ")
        labelX.setFont(QtGui.QFont("Calibri", 10))
        lineX = QtWidgets.QLineEdit()
        lineX.setMaximumSize(50, 21)
        lineX.setFont(QtGui.QFont("Calibri", 10))

        graphTBtn = QPushButton()
        graphTBtn.setText("Graficar tendencias")
        graphTBtn.setFont(QtGui.QFont("Calibri", 10))
        graphTBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        graphTBtn.clicked.connect(lambda: self.tendencies(lineX.text()))

        hLayout = QHBoxLayout()
        hLayout.addWidget(labelX)
        hLayout.addWidget(lineX)
        hLayout.addWidget(graphTBtn)
        hLayoutElm = QWidget()
        hLayoutElm.setLayout(hLayout)

        self.layout.addWidget(canvasElmt, 2)
        self.layout.addWidget(element, 1)
        self.layout.addWidget(hLayoutElm)
        
        if len(self.layout) > 7:
            self.layout.itemAt(len(self.layout)-5).widget().deleteLater()

    def tendencies(self, xAxis):
        global datos
        x = datos[xAxis]
        names = []

        figure = plt.figure(figsize=(12,8))
        for y in conjuntoDatos:
            plt.plot(x,y,marker='o')
            names.append(y.name)
        plt.legend(names, prop = {'size':10},loc='lower right')
        plt.xlabel(xAxis)
        plt.ylabel('')

        canvas = FigureCanvasQTAgg(figure)
        toolbar = NavigationToolbar2QT(canvas, self)
        canvLayout = QVBoxLayout()
        canvLayout.addWidget(toolbar)
        canvLayout.addWidget(canvas)
        canvasElmt = QWidget()
        canvasElmt.setLayout(canvLayout)
        canvasElmt.setMinimumSize(300, 480) 

        self.layout.addWidget(canvasElmt)

    def clearLayout(self):
        for i in reversed(range(self.layout.count())): 
            if self.layout.itemAt(i).widget() is not None:
                self.layout.itemAt(i).widget().deleteLater()
            elif self.layout.itemAt(i).widget() is None:
                self.layout.removeItem(self.layout.itemAt(i))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Stats()
    ui.show()
    sys.exit(app.exec_())
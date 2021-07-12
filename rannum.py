from os import name
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp, fixed, pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QBoxLayout, QColorDialog, QComboBox, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLayout, QMainWindow, QPushButton, QScrollArea, QSpacerItem, QTabWidget, QTableView, QVBoxLayout, QWIDGETSIZE_MAX, QWidget, QInputDialog, QLineEdit, QFileDialog, QMdiSubWindow
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

class RandNum(QMainWindow):

    def __init__(self):
        super(RandNum, self).__init__()
        self.resize(813, 700)

        self.colorDialog = QColorDialog(self)

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)

        self.centralwidget = QWidget(self)

        self.dropDown = QComboBox()
        self.dropDown.setFont(font)
        self.dropDown.addItem("Cuadrados Medios")
        self.dropDown.addItem("Congruencial Lineal")
        self.dropDown.addItem("Congruencial Multiplicativo")
        self.dropDown.addItem("Borland C/C++")
        self.dropDown.addItem("Python")
        self.dropDown.addItem("Numpy")
        self.dropDown.resize(200, 50)

        self.genBtn = QPushButton("Generar")
        self.genBtn.clicked.connect(lambda: self.option())  
        self.genBtn.resize(100, 50)

        self.newBtn = QPushButton("New")
        self.newBtn.clicked.connect(lambda: self.clearLayout())

        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(self.dropDown)
        self.hLayout.addWidget(self.genBtn)
        self.hLayout.addWidget(self.newBtn)
        self.input = QWidget()
        self.input.setLayout(self.hLayout)

        self.outLayout = QVBoxLayout()
        self.container = QWidget(self.centralwidget)
        self.container.setMinimumSize(795, 640)
        self.vLayout = QVBoxLayout()
        self.output = QWidget(self.container)
        scrollArea = QScrollArea()
        scrollArea.setWidget(self.output)
        scrollArea.setMinimumSize(500, 50)
        scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scrollArea.setWidgetResizable(True)
        self.outLayout.addWidget(scrollArea)
        self.container.setLayout(self.outLayout)
        self.output.setLayout(self.vLayout)

        self.layout = QVBoxLayout(self.centralwidget)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.container)
        self.layout.addStretch()

        self.setCentralWidget(self.centralwidget)

    def option(self):
        option = self.dropDown.currentText()
        
        if option == "Cuadrados Medios":
            self.cuadradosMediosInput()
        elif option == "Congruencial Lineal":
            self.cuadradosMediosInput()

    def cuadradosMediosInput(self):
        self.clearLayout()
        
        lableSeed = QLabel("Ingrese una semilla: ")
        lineSeed = QLineEdit()

        hLayout = QHBoxLayout()
        hLayout.addWidget(lableSeed)
        hLayout.addWidget(lineSeed)
        hWidget = QWidget()
        hWidget.setLayout(hLayout)

        lableQtty = QLabel("Ingrese una cantidad: ")
        lineQtty = QLineEdit()
        btnInput = QPushButton("Ok") 
        btnInput.clicked.connect(lambda: self.cuadradosMediosOutput(int(lineQtty.text()), int(lineSeed.text())))

        hLayout2 = QHBoxLayout()
        hLayout2.addWidget(lableQtty)
        hLayout2.addWidget(lineQtty)
        hLayout2.addWidget(btnInput)
        hWidget2 = QWidget()
        hWidget2.setLayout(hLayout2)

        self.vLayout.addWidget(hWidget)    
        self.vLayout.addWidget(hWidget2)
        self.vLayout.addStretch()    

    def cuadradosMediosOutput(self, qtty, seed):
    # Método de los cuadrados medios
        n=qtty
        #r=7182
        # seleccionamos el valor inicial r
        r=seed
        # seleccionamos el valor inicial r
        l=len(str(r))
        # determinamos el número de dígitos
        lista = []
        # almacenamos en una lista
        lista2 = []
        i=1
        #while len(lista) == len(set(lista)):
        while i < n:
            x=str(r*r)
            # Elevamos al cuadrado r
            if l % 2 == 0:
                x = x.zfill(l*2)
            else:
                x = x.zfill(l)
            y=(len(x)-l)/2
            y=int(y)
            r=int(x[y:y+l])
            lista.append(r)
            lista2.append(x)
            i=i+1
        df = pd.DataFrame({'X2':lista2,'Xi':lista})
        dfrac = df["Xi"]/10**l
        df["ri"] = dfrac
        #df.head()
        df 

        model = mod(df)
        table = QTableView()
        table.setMinimumSize(750, 200)
        table.setMaximumSize(750, 200)
        table.setModel(model)

        figure = plt.figure(figsize=(12,8))
        x1=df['ri']
        plt.plot(x1)
        plt.title('Generador de Numeros Aleatorios Cuadrados Medios')
        plt.xlabel('Serie')
        plt.ylabel('Aleatorios')
        canvas = FigureCanvasQTAgg(figure)
        toolbar = NavigationToolbar2QT(canvas, self)
        canvLayout = QVBoxLayout()
        canvLayout.addWidget(toolbar)
        canvLayout.addWidget(canvas)
        canvasElmt = QWidget()
        canvasElmt.setLayout(canvLayout)
        canvasElmt.setMinimumSize(300, 480) 

        self.vLayout.addWidget(table)
        self.vLayout.addWidget(canvasElmt)

    def clearLayout(self):
        for i in reversed(range(self.vLayout.count())): 
            if self.vLayout.itemAt(i).widget() is not None:
                self.vLayout.itemAt(i).widget().deleteLater()
            elif self.vLayout.itemAt(i).widget() is None:
                self.vLayout.removeItem(self.vLayout.itemAt(i))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = RandNum()
    ui.show()
    sys.exit(app.exec_())
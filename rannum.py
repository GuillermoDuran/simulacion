from datetime import datetime, date
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction, QComboBox, QHBoxLayout, QLabel, QMainWindow, QMessageBox, QPushButton, QScrollArea, QTableView, QVBoxLayout, QWidget, QLineEdit
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import dfModel
mod = dfModel.DataFrameModel

class RandNum(QMainWindow):

    def __init__(self):
        
        super(RandNum, self).__init__()
        self.resize(813, 700)
        self.setWindowTitle('Números aleatorios')

        quit = QAction('Quit', self)

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)

        self.centralwidget = QWidget(self)

        self.dropDown = QComboBox()
        self.dropDown.setFont(font)
        self.dropDown.addItem("Cuadrados Medios")
        self.dropDown.addItem("Congruencial Lineal")
        self.dropDown.addItem("Congruencial Multiplicativo")
        self.dropDown.addItem("Numpy")
        self.dropDown.resize(200, 50)

        self.genBtn = QPushButton("Generar")
        self.genBtn.clicked.connect(lambda: self.option())  
        self.genBtn.resize(100, 50)

        self.newBtn = QPushButton("Borrar todo")
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
            self.congruencialLinealInput()
        elif option == "Congruencial Multiplicativo":
            self.congruencialMultiplicativoInput()
        elif option == "Numpy":
            self.numpyInput()

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
        btnInput.clicked.connect(lambda: self.cuadradosMediosOutput(lineQtty.text(), lineSeed.text()))

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

        while True:
            try:
                # Método de los cuadrados medios
                n=int(qtty)
                #r=7182
                # seleccionamos el valor inicial r
                r=float(seed)
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

                model = mod(df)
                table = QTableView()
                table.setMinimumSize(750, 200)
                table.setMaximumSize(750, 200)
                table.setModel(model)

                labelFileName = QLabel('Nombre del archivo (opcional): ')
                inputFileName = QLineEdit()

                btnSaveCsv = QPushButton('Guardar')
                btnSaveCsv.clicked.connect(lambda: self.saveCsv(df, inputFileName.text(), 'cuadrados_medios_'))

                hLayout = QHBoxLayout()
                hLayout.addWidget(labelFileName)
                hLayout.addWidget(inputFileName)
                hLayout.addWidget(btnSaveCsv)
                hWidget = QWidget()
                hWidget.setLayout(hLayout)

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
                self.vLayout.addWidget(hWidget)
                self.vLayout.addWidget(canvasElmt)

                break
            except ValueError:
                dlg = QMessageBox(self)
                dlg.setWindowTitle('Error')
                dlg.setText('Existen campos vacios o ha ingresado datos incorrectos')
                dlg.setIcon(QMessageBox.Information)
                btn = dlg.exec()

                break

    def congruencialLinealInput(self):

        self.clearLayout()
        lableSeed = QLabel("Semilla: ")
        lineSeed = QLineEdit()

        lableMultiplier = QLabel("Multiplicador: ")
        lineMultiplier = QLineEdit()

        hLayout = QHBoxLayout()
        hLayout.addWidget(lableSeed)
        hLayout.addWidget(lineSeed)
        hLayout.addWidget(lableMultiplier)
        hLayout.addWidget(lineMultiplier)
        hWidget = QWidget()
        hWidget.setLayout(hLayout)

        lableModule = QLabel("Módulo: ")
        lineModule = QLineEdit()

        lableIncrement = QLabel("Incremento: ")
        lineIncrement = QLineEdit()

        hLayout0 = QHBoxLayout()
        hLayout0.addWidget(lableModule)
        hLayout0.addWidget(lineModule)
        hLayout0.addWidget(lableIncrement)
        hLayout0.addWidget(lineIncrement)
        hWidget0 = QWidget()
        hWidget0.setLayout(hLayout0)

        lableQtty = QLabel("Cantidad: ")
        lineQtty = QLineEdit()

        btnInput = QPushButton("Ok") 
        btnInput.clicked.connect(lambda: self.congruencialLinealOutput(lineQtty.text(), lineSeed.text(),
                                lineMultiplier.text(), lineModule.text(), lineIncrement.text()))

        hLayout1 = QHBoxLayout()
        hLayout1.addWidget(lableQtty)
        hLayout1.addWidget(lineQtty)
        hLayout1.addWidget(btnInput)
        hWidget1 = QWidget()
        hWidget1.setLayout(hLayout1)

        self.vLayout.addWidget(hWidget)    
        self.vLayout.addWidget(hWidget0)
        self.vLayout.addWidget(hWidget1)
        self.vLayout.addStretch()

    def congruencialLinealOutput(self, qtty, seed, multiplier, module, increment):

        while True:
            try:
                qtty = int(qtty)
                seed = float(seed)
                multiplier = float(multiplier)
                module = float(module)
                increment = float(increment)

                if module < 0 or module < multiplier or module < increment:
                    dlg = QMessageBox(self)
                    dlg.setWindowTitle('Error')
                    dlg.setText('El módulo tiene que ser mayor > 0, > multiplicador, > incremento')
                    dlg.setIcon(QMessageBox.Information)
                    btn = dlg.exec()

                    break
                else: 
                    n, m, a, x0, c = qtty, module, multiplier, seed, increment
                    x = [1] * n
                    r = [0.1] * n

                    for i in range(0, n):
                        x[i] = ((a*x0)+c) % m
                        x0 = x[i]
                        r[i] = round(x0 / m, 4)

                    d = {'Xn': x, 'ri': r }
                    df = pd.DataFrame(data=d)

                    model = mod(df)
                    table = QTableView()
                    table.setMinimumSize(750, 200)
                    table.setMaximumSize(750, 200)
                    table.setModel(model)

                    figure = plt.figure(figsize=(12,8))
                    x1=df['ri']
                    plt.plot(x1)
                    plt.title('Generador de Numeros Aleatorios Congruencial Lineal')
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

                    labelFileName = QLabel('Nombre del archivo (opcional): ')
                    inputFileName = QLineEdit()

                    btnSaveCsv = QPushButton('Guardar')
                    btnSaveCsv.clicked.connect(lambda: self.saveCsv(df, inputFileName.text(), 'congruencial_lineal_'))

                    hLayout = QHBoxLayout()
                    hLayout.addWidget(labelFileName)
                    hLayout.addWidget(inputFileName)
                    hLayout.addWidget(btnSaveCsv)
                    hWidget = QWidget()
                    hWidget.setLayout(hLayout)

                    self.vLayout.addWidget(table)
                    self.vLayout.addWidget(hWidget)
                    self.vLayout.addWidget(canvasElmt)

                    break
            except ValueError:
                dlg = QMessageBox(self)
                dlg.setWindowTitle('Error')
                dlg.setText('Existen campos vacios o ha ingresado datos incorrectos')
                dlg.setIcon(QMessageBox.Information)
                btn = dlg.exec()

                break

    def congruencialMultiplicativoInput(self):
        self.clearLayout()
        lableSeed = QLabel("Semilla: ")
        lineSeed = QLineEdit()

        lableMultiplier = QLabel("Multiplicador: ")
        lineMultiplier = QLineEdit()

        hLayout = QHBoxLayout()
        hLayout.addWidget(lableSeed)
        hLayout.addWidget(lineSeed)
        hLayout.addWidget(lableMultiplier)
        hLayout.addWidget(lineMultiplier)
        hWidget = QWidget()
        hWidget.setLayout(hLayout)

        lableModule = QLabel("Módulo: ")
        lineModule = QLineEdit()

        lableQtty = QLabel("Cantidad: ")
        lineQtty = QLineEdit()

        btnInput = QPushButton("Ok") 
        btnInput.clicked.connect(lambda: self.congruencialMultiplicativoOutput(lineQtty.text(), lineSeed.text(),
                                lineMultiplier.text(), lineModule.text()))

        hLayout0 = QHBoxLayout()
        hLayout0.addWidget(lableModule)
        hLayout0.addWidget(lineModule)
        hLayout0.addWidget(lableQtty)
        hLayout0.addWidget(lineQtty)
        hLayout0.addWidget(btnInput)
        hWidget0 = QWidget()
        hWidget0.setLayout(hLayout0)

        self.vLayout.addWidget(hWidget)    
        self.vLayout.addWidget(hWidget0)
        self.vLayout.addStretch()

    def congruencialMultiplicativoOutput(self, qtty, seed, multiplier, module):

        while True:
            try:
                qtty = int(qtty)
                seed = float(seed)
                multiplier = float(multiplier)
                module = float(module)

                if module < 0 or module < multiplier:
                    dlg = QMessageBox(self)
                    dlg.setWindowTitle('Error')
                    dlg.setText('El módulo tiene que ser mayor > 0, > multiplicador')
                    dlg.setIcon(QMessageBox.Information)
                    btn = dlg.exec()
                else: 
                    n, m, a, x0 = qtty, module, multiplier, seed
                    x = [1] * n
                    r = [0.1] * n
                    for i in range(0, n):
                        x[i] = (a*x0) % m
                        x0 = x[i]
                        r[i] = round(x0 / m, 4)
                    d = {'Xn': x, 'ri': r }
                    df = pd.DataFrame(data=d)

                    model = mod(df)
                    table = QTableView()
                    table.setMinimumSize(750, 200)
                    table.setMaximumSize(750, 200)
                    table.setModel(model)

                    figure = plt.figure(figsize=(12,8))
                    x1=df['ri']
                    plt.plot(x1)
                    plt.title('Generador de Numeros Aleatorios Congruencial Multiplicativo')
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

                    labelFileName = QLabel('Nombre del archivo (opcional): ')
                    inputFileName = QLineEdit()

                    btnSaveCsv = QPushButton('Guardar')
                    btnSaveCsv.clicked.connect(lambda: self.saveCsv(df, inputFileName.text(), 'congruencial_multiplicativo_'))

                    hLayout = QHBoxLayout()
                    hLayout.addWidget(labelFileName)
                    hLayout.addWidget(inputFileName)
                    hLayout.addWidget(btnSaveCsv)
                    hWidget = QWidget()
                    hWidget.setLayout(hLayout)

                    self.vLayout.addWidget(table)
                    self.vLayout.addWidget(hWidget)
                    self.vLayout.addWidget(canvasElmt)

                    break
            except ValueError:
                dlg = QMessageBox(self)
                dlg.setWindowTitle('Error')
                dlg.setText('Existen campos vacios o ha ingresado datos incorrectos')
                dlg.setIcon(QMessageBox.Information)
                btn = dlg.exec()

                break

    def numpyInput(self):
        self.clearLayout()
        lableSeed = QLabel("Semilla: ")
        lineSeed = QLineEdit()

        lableQuantity = QLabel("Cantidad: ")
        lineQuantity = QLineEdit()
        
        btnInput = QPushButton("Ok") 
        btnInput.clicked.connect(lambda: self.numpyOutput(lineQuantity.text(), lineSeed.text()))

        hLayout = QHBoxLayout()
        hLayout.addWidget(lableSeed)
        hLayout.addWidget(lineSeed)
        hLayout.addWidget(lableQuantity)
        hLayout.addWidget(lineQuantity)
        hLayout.addWidget(btnInput)
        hWidget = QWidget()
        hWidget.setLayout(hLayout)

        self.vLayout.addWidget(hWidget)
        self.vLayout.addStretch()

    def numpyOutput(self, qtty, seed):

        while True:
            try:
                qtty = int(qtty)
                seed = int(seed)

                np.random.seed(seed)
                x = np.random.rand(qtty)
                df = pd.DataFrame({'Xn': x})

                model = mod(df.round(4))
                table = QTableView()
                table.setMinimumSize(750, 200)
                table.setMaximumSize(750, 200)
                table.setModel(model)

                figure = plt.figure(figsize=(12,8))
                x1=df['Xn']
                plt.plot(x1)
                plt.title('Generador de Numeros Aleatorios Python Numpy')
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

                labelFileName = QLabel('Nombre del archivo (opcional): ')
                inputFileName = QLineEdit()

                btnSaveCsv = QPushButton('Guardar')
                btnSaveCsv.clicked.connect(lambda: self.saveCsv(df, inputFileName.text(), 'numpy_'))

                hLayout = QHBoxLayout()
                hLayout.addWidget(labelFileName)
                hLayout.addWidget(inputFileName)
                hLayout.addWidget(btnSaveCsv)
                hWidget = QWidget()
                hWidget.setLayout(hLayout)

                self.vLayout.addWidget(table)
                self.vLayout.addWidget(canvasElmt)

                break
            except ValueError:
                dlg = QMessageBox(self)
                dlg.setWindowTitle('Error')
                dlg.setText('Existen campos vacios o ha ingresado datos incorrectos')
                dlg.setIcon(QMessageBox.Information)
                btn = dlg.exec()

                break

    def saveCsv(self, df, name, simType):
        if name == '':
            dt = datetime.now()
            ts = datetime.timestamp(dt)
            d = date.fromtimestamp(ts)

            df.to_csv(simType+str(d)+str(int(ts))+'.csv', index = False)
        else: 
            df.to_csv(name+'.csv')

    def clearLayout(self):
        for i in reversed(range(self.vLayout.count())): 
            if self.vLayout.itemAt(i).widget() is not None:
                self.vLayout.itemAt(i).widget().deleteLater()
            elif self.vLayout.itemAt(i).widget() is None:
                self.vLayout.removeItem(self.vLayout.itemAt(i))

    def closeWindow(self, main):
        self.close
        main.setEnabled(True)

if __name__ == "__rannum__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = RandNum()
    ui.show()
    sys.exit(app.exec_())
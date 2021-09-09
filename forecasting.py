from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime, date
from PyQt5.QtWidgets import QComboBox, QFileDialog, QHBoxLayout, QLabel, QMainWindow, QMessageBox, QPushButton, QScrollArea, QTableView, QVBoxLayout, QWidget, QLineEdit
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import dfModel
mod = dfModel.DataFrameModel

class Forecasting(QMainWindow):

    def __init__(self):

        super(Forecasting, self).__init__()
        self.resize(813, 700)
        self.setWindowTitle('Pronósticos')

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)

        self.centralwidget = QWidget(self)

        self.lineFilePath = QLineEdit()
        self.lineFilePath.setReadOnly(True)

        self.fileBtn = QPushButton('Seleccionar archivo...')
        self.fileBtn.clicked.connect(lambda: self.openFileDialog(self.lineFilePath))

        self.showTblBtn = QPushButton('Mostrar tabla')
        self.showTblBtn.clicked.connect(lambda: self.showTable(self.lineFilePath.text()))

        self.newBtn = QPushButton("Borrar todo")
        self.newBtn.clicked.connect(lambda: self.clearLayout())

        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(self.fileBtn)
        self.hLayout.addWidget(self.lineFilePath)
        self.hLayout.addWidget(self.showTblBtn)
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

    def openFileDialog(self, lineFilePath):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","CSV files (*.csv)", options=options)
        if fileName:
            lineFilePath.setText(fileName)

    def showTable(self, file):

        self.clearLayout()

        if file != '':
            df = pd.read_csv(file)

            model = mod(df)
            tableMovil = QTableView()
            tableMovil.setMinimumSize(750, 200)
            tableMovil.setMaximumSize(750, 200)
            tableMovil.setModel(model)

            font = QtGui.QFont()
            font.setFamily("Calibri")
            font.setPointSize(10)

            dropDown = QComboBox()
            dropDown.setFont(font)
            dropDown.addItem("Promedio Móvil")
            dropDown.addItem("Suavización Exponencial")
            dropDown.addItem("Regresión Lineal")
            dropDown.addItem("Regresión Cuadrada")
            dropDown.resize(200, 50)

            forecastBtn = QPushButton("Pronosticar")
            forecastBtn.clicked.connect(lambda: self.options(df, dropDown.currentText()))
            forecastBtn.resize(100, 50)

            clearBtn = QPushButton("Borrar salida")
            clearBtn.clicked.connect(lambda: self.clearOutput())

            vLayout = QVBoxLayout()
            vLayout.addWidget(tableMovil)

            hLayout = QHBoxLayout()
            hLayout.addWidget(dropDown)
            hLayout.addWidget(forecastBtn)
            hLayout.addWidget(clearBtn)
            hBtnGroup = QWidget()
            hBtnGroup.setLayout(hLayout)

            vLayout.addWidget(hBtnGroup)

            tableElms = QWidget()
            tableElms.setLayout(vLayout)

            self.vLayout.addWidget(tableElms)
            self.vLayout.addStretch()
        else: 
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Error')
            dlg.setText('Seleccione un documento')
            dlg.setIcon(QMessageBox.Information)
            btn = dlg.exec()

    def options(self, df, option):
        
        if option == "Promedio Móvil":
            self.promedioMovilOutput(df)
        elif option == "Suavización Exponencial":
            self.suavizacionExpOutput(df)
        elif option == "Regresión Lineal":
            self.regresionLinealOutput(df)
        elif option == "Regresión Cuadrada":
            self.regresionCuadradaOutput(df)

    def promedioMovilOutput(self, df):

        self.clearOutput()

        movil = df.copy()

        # calculamos para la primera media móvil MMO_3

        for i in range(0,movil.shape[0]-2):
            movil.loc[movil.index[i+2],'MMO_3'] = np.round(((movil.iloc[i,1]+movil.iloc[i+1,1]+movil.iloc[i+2,1])/3),1)

        # calculamos para la segunda media móvil MMO_4    
        for i in range(0,movil.shape[0]-3):
            movil.loc[movil.index[i+3],'MMO_4'] = np.round(((movil.iloc[i,1]+movil.iloc[i+1,1]+movil.iloc[i+2,1]+movil.iloc[i+3,1])/4),1)

        # calculamos la proyeción final

        proyeccion = movil.iloc[12:,[1,2,3]]
        p1,p2,p3 =proyeccion.mean()
        # incorporamos al DataFrame
        a = movil.append({movil.columns[0]:2018, movil.columns[1]:p1, 'MMO_3':p2, 'MMO_4':p3},ignore_index=True)
        # mostramos los resultados

        a['e_MM3'] = a[movil.columns[1]]-a['MMO_3']
        a['e_MM4'] = a[movil.columns[1]]-a['MMO_4']

        aModel = mod(a)
        tableA = QTableView()
        tableA.setMinimumSize(750, 200)
        tableA.setMaximumSize(750, 200)
        tableA.setModel(aModel)

        labelFileName = QLabel('Nombre del archivo (opcional): ')
        inputFileName = QLineEdit()

        btnSaveCsv = QPushButton('Guardar')
        btnSaveCsv.clicked.connect(lambda: self.saveCsv(a, inputFileName.text(), 'promedio_movil_'))

        hLayout = QHBoxLayout()
        hLayout.addWidget(labelFileName)
        hLayout.addWidget(inputFileName)
        hLayout.addWidget(btnSaveCsv)
        hWidget = QWidget()
        hWidget.setLayout(hLayout)

        figure = plt.figure(figsize=(12,8))
        plt.grid(True)
        plt.plot(a[movil.columns[1]],label=movil.columns[1],marker='o')
        plt.plot(a['MMO_3'],label='Media Móvil 3 años')
        plt.plot(a['MMO_4'],label='Media Móvil 4 años')
        plt.legend(loc=2)
        canvas = FigureCanvasQTAgg(figure)
        toolbar = NavigationToolbar2QT(canvas, self)
        canvLayout = QVBoxLayout()
        canvLayout.addWidget(toolbar)
        canvLayout.addWidget(canvas)
        canvasElmt = QWidget()
        canvasElmt.setLayout(canvLayout)
        canvasElmt.setMinimumSize(300, 480) 

        self.vLayout.addWidget(tableA)
        self.vLayout.addWidget(hWidget)
        self.vLayout.addWidget(canvasElmt)

    def suavizacionExpOutput(self, df):

        data = df.copy()

        self.clearOutput()

        alfa = 0.1
        unoalfa = 1. - alfa

        for i in range(0,data.shape[0]-1):
            data.loc[data.index[i+1],'SN'] = np.round(data.iloc[i,1],1)

        for i in range(2,data.shape[0]):
            data.loc[data.index[i],'SN'] = np.round(data.iloc[i-1,1],1)*alfa + np.round(data.iloc[i-1,2],1)*unoalfa
        i=i+1
        p1=0
        p2=np.round(data.iloc[i-1,1],1)*alfa + np.round(data.iloc[i-1,2],1)*unoalfa
        a1 = data.append({data.columns[0]:2018, data.columns[1]:p1, 'SN':p2},ignore_index=True)

        sExpModel = mod(a1)
        tableSExp = QTableView()
        tableSExp.setMinimumSize(750, 200)
        tableSExp.setMaximumSize(750, 200)
        tableSExp.setModel(sExpModel)

        labelFileName = QLabel('Nombre del archivo (opcional): ')
        inputFileName = QLineEdit()

        btnSaveCsv = QPushButton('Guardar')
        btnSaveCsv.clicked.connect(lambda: self.saveCsv(a1, inputFileName.text(), 'suavizacion_exponencial_'))

        hLayout = QHBoxLayout()
        hLayout.addWidget(labelFileName)
        hLayout.addWidget(inputFileName)
        hLayout.addWidget(btnSaveCsv)
        hWidget = QWidget()
        hWidget.setLayout(hLayout)

        figure = plt.figure(figsize=(12,8))
        plt.grid(True)
        plt.plot(a1[data.columns[1]],label=data.columns[1],marker='o')
        plt.plot(a1['SN'],label='SN')
        plt.legend(loc=2)
        canvas = FigureCanvasQTAgg(figure)
        toolbar = NavigationToolbar2QT(canvas, self)
        canvLayout = QVBoxLayout()
        canvLayout.addWidget(toolbar)
        canvLayout.addWidget(canvas)
        canvasElmt = QWidget()
        canvasElmt.setLayout(canvLayout)
        canvasElmt.setMinimumSize(300, 480)

        self.vLayout.addWidget(tableSExp)
        self.vLayout.addWidget(canvasElmt)
        self.vLayout.addWidget(hWidget)
        self.vLayout.addStretch()

    def regresionLinealOutput(self, df):

        data = df.copy()

        self.clearOutput()

        x = data.index.values
        y= data[data.columns[1]]
        # ajuste de la recta (polinomio de grado 1  f(x) = ax + b)
        p = np.polyfit(x,y,1)  # 1 para lineal, 2 para polinomio ...

        y_ajuste = p[0]*x + p[1]

        data['y_ajuste'] = y_ajuste

        tableModel = mod(data)
        table = QTableView()
        table.setMinimumSize(750, 200)
        table.setMaximumSize(750, 200)
        table.setModel(tableModel)

        labelFileName = QLabel('Nombre del archivo (opcional): ')
        inputFileName = QLineEdit()

        btnSaveCsv = QPushButton('Guardar')
        btnSaveCsv.clicked.connect(lambda: self.saveCsv(data, inputFileName.text(), 'regresion_lineal_'))

        hLayout = QHBoxLayout()
        hLayout.addWidget(labelFileName)
        hLayout.addWidget(inputFileName)
        hLayout.addWidget(btnSaveCsv)
        hWidget = QWidget()
        hWidget.setLayout(hLayout)

        figure = plt.figure(figsize=(12,8))
        # dibujamos los datos experimentales de la recta 
        plt.plot(x,y,'b.')
        # Dibujamos la recta de ajuste
        plt.plot(x,y_ajuste, 'r-')
        plt.title('Ajuste lineal por mínimos cuadrados')
        plt.xlabel('Eje x')
        plt.ylabel('Eje y')
        plt.legend(('Datos experimentales','Ajuste lineal',), loc="upper left")
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
        self.vLayout.addStretch()

    def regresionCuadradaOutput(self, df):

        data = df.copy()

        self.clearOutput()

        x = data.index.values
        y= data[data.columns[1]]

        p = np.polyfit(x,y,2)

        y_ajuste = p[0]*x*x + p[1]*x + p[2]

        data['y_ajuste'] = y_ajuste

        tableModel = mod(data)
        table = QTableView()
        table.setMinimumSize(750, 200)
        table.setMaximumSize(750, 200)
        table.setModel(tableModel)

        labelFileName = QLabel('Nombre del archivo (opcional): ')
        inputFileName = QLineEdit()

        btnSaveCsv = QPushButton('Guardar')
        btnSaveCsv.clicked.connect(lambda: self.saveCsv(data, inputFileName.text(), 'regresion_cuadratica_'))

        hLayout = QHBoxLayout()
        hLayout.addWidget(labelFileName)
        hLayout.addWidget(inputFileName)
        hLayout.addWidget(btnSaveCsv)
        hWidget = QWidget()
        hWidget.setLayout(hLayout)

        figure = plt.figure(figsize=(12,8))
        # dibujamos los datos experimentales de la recta 
        plt.plot(x,y,'b.')
        # Dibujamos la curva de ajuste
        plt.plot(x,y_ajuste, 'r-')
        plt.title('Ajuste Polinomial por mínimos cuadrados')
        plt.xlabel('Eje x')
        plt.ylabel('Eje y')
        plt.legend(('Datos experimentales','Ajuste Polinomial',), loc="upper left")
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
        self.vLayout.addStretch()

    def saveCsv(self, df, name, simType):
        if name == '':
            dt = datetime.now()
            ts = datetime.timestamp(dt)
            d = date.fromtimestamp(ts)

            df.to_csv(simType+str(d)+str(int(ts))+'.csv', index = False)
        else: 
            df.to_csv(name+'.csv')

    def clearOutput(self):

        for i in reversed(range(self.vLayout.count())): 
            if i > 1:
                if self.vLayout.itemAt(i).widget() is not None:
                    self.vLayout.itemAt(i).widget().deleteLater()
                elif self.vLayout.itemAt(i).widget() is None:
                    self.vLayout.removeItem(self.vLayout.itemAt(i))

    def clearLayout(self):

        for i in reversed(range(self.vLayout.count())): 
            if self.vLayout.itemAt(i).widget() is not None:
                self.vLayout.itemAt(i).widget().deleteLater()
            elif self.vLayout.itemAt(i).widget() is None:
                self.vLayout.removeItem(self.vLayout.itemAt(i))

if __name__ == "__forecasting__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Forecasting()
    ui.show()
    sys.exit(app.exec_())
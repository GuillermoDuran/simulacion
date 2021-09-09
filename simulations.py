import random
from datetime import datetime, date
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QComboBox, QFileDialog, QHBoxLayout, QLabel, QMainWindow, QPushButton, QScrollArea, QTableView, QVBoxLayout, QWidget, QLineEdit, QMessageBox
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import itertools

import dfModel
import pdModel

class Simulation(QMainWindow):

    def __init__(self):

        super(Simulation, self).__init__()
        self.resize(813, 700)
        self.setWindowTitle('Simulación')

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)

        self.centralwidget = QWidget(self)

        self.dropDown = QComboBox()
        self.dropDown.setFont(font)
        self.dropDown.addItem("Montecarlo")
        self.dropDown.addItem("Inventario")
        self.dropDown.addItem("Linea de espera")
        self.dropDown.resize(200, 50)

        self.forecastBtn = QPushButton("Ok")
        self.forecastBtn.clicked.connect(lambda: self.options(self.dropDown.currentText()))
        self.forecastBtn.resize(100, 50)

        self.clearBtn = QPushButton('Borrar todo')
        self.clearBtn.clicked.connect(lambda: self.clearLayout())

        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(self.dropDown)
        self.hLayout.addWidget(self.forecastBtn)
        self.hLayout.addWidget(self.clearBtn)
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

    def options(self, option):
        
        if option == "Montecarlo":
            self.selectFile()
        elif option == "Inventario":
            self.simInventarioInput()
        elif option == "Linea de espera":
            self.simLineaEsperaInput()

    def selectFile(self):

        self.clearLayout()

        index = self.vLayout.count()+1
        
        lineFilePath = QLineEdit()
        lineFilePath.setReadOnly(True)

        fileBtn = QPushButton('Seleccionar archivo...')
        fileBtn.clicked.connect(lambda: self.openFileDialog(lineFilePath))

        showTblBtn = QPushButton('Mostrar tabla')
        showTblBtn.clicked.connect(lambda: self.showTable(lineFilePath.text()))

        newBtn = QPushButton("Borrar salida")
        newBtn.clicked.connect(lambda: self.clearOutput(index))

        hLayout = QHBoxLayout()
        hLayout.addWidget(fileBtn)
        hLayout.addWidget(lineFilePath)
        hLayout.addWidget(showTblBtn)
        hLayout.addWidget(newBtn)
        
        hWidget = QWidget()
        hWidget.setLayout(hLayout)

        self.vLayout.addWidget(hWidget)
        self.vLayout.addStretch()

    def openFileDialog(self, lineFilePath):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","CSV files (*.csv)", options=options)
        if fileName:
            lineFilePath.setText(fileName)

    def showTable(self, file):

        if file == '':
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Error')
            dlg.setText('Seleccione un documento')
            dlg.setIcon(QMessageBox.Information)
            btn = dlg.exec()
        else:
            index = self.vLayout.count()+1
            self.clearOutput(index)

            df = pd.read_csv(file, delimiter=',', encoding="utf-8-sig")

            model = dfModel.DataFrameModel(df)
            tableMovil = QTableView()
            tableMovil.setMinimumSize(750, 200)
            tableMovil.setMaximumSize(750, 200)
            tableMovil.setModel(model)

            font = QtGui.QFont()
            font.setFamily("Calibri")
            font.setPointSize(10)

            simBtn = QPushButton('Siguiente')
            simBtn.clicked.connect(lambda: self.simMontecarloInput(df))

            clearBtn = QPushButton("Borrar salida")
            clearBtn.clicked.connect(lambda: self.clearOutput(index))

            vLayout = QVBoxLayout()
            vLayout.addWidget(tableMovil)

            hLayout = QHBoxLayout()
            hLayout.addWidget(simBtn)
            hLayout.addWidget(clearBtn)
            hBtnGroup = QWidget()
            hBtnGroup.setLayout(hLayout)

            vLayout.addWidget(hBtnGroup)

            tableElms = QWidget()
            tableElms.setLayout(vLayout)

            inLayout = QVBoxLayout()
            inLayout.addWidget(tableElms)
            inLayout.addWidget(hBtnGroup)
            inWidget = QWidget()
            inWidget.setLayout(inLayout)

            self.vLayout.addWidget(inWidget, 1)
            self.vLayout.addStretch(1)

    def simMontecarloInput(self, df):

        index = self.vLayout.count()+1

        timeLabel = QLabel('Periodo de tiempo:')
        timeInput = QComboBox()
        for column in df.columns:
            timeInput.addItem(column)
        timeInput.resize(200, 50)

        dataLabel = QLabel('Dato a simular:')
        dataInput = QComboBox()
        for column in df.columns:
            dataInput.addItem(column)
        dataInput.resize(200, 50)

        qttyLabel = QLabel('Cantidad de simulaciones: ')
        qttyInput = QLineEdit()

        simBtn = QPushButton('Simular')
        simBtn.clicked.connect(lambda: self.simMontecarloOutput(df, timeInput.currentText(), dataInput.currentText(), qttyInput.text()))

        clearBtn = QPushButton("Borrar salida")
        clearBtn.clicked.connect(lambda: self.clearOutput(index))

        vLayout = QVBoxLayout()

        hLayout = QHBoxLayout()
        hLayout.addWidget(timeLabel)
        hLayout.addWidget(timeInput)
        hLayout.addWidget(dataLabel)
        hLayout.addWidget(dataInput)
        hLayout.addWidget(qttyLabel)
        hLayout.addWidget(qttyInput)
        hWidget = QWidget()
        hWidget.setLayout(hLayout)

        vLayout.addWidget(hWidget)
        vLayout.addWidget(simBtn)
        vWidget = QWidget()
        vWidget.setLayout(vLayout)

        self.vLayout.addWidget(vWidget, 1)
        self.vLayout.addStretch(1)

    def simMontecarloOutput(self, df, timeFrame, simData, qtty):

        if qtty == '' or not qtty.isdigit():
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Error')
            dlg.setText('Ingrese un numero entero para la cantidad')
            dlg.setIcon(QMessageBox.Information)
            btn = dlg.exec()
        else:
            dfCopy = df.copy()

            demanda = dfCopy.filter(items = [timeFrame, simData])

            demandas = demanda.groupby(timeFrame)
            demandas.sum()
            
            tot = demandas.mean()
            
            suma = tot[simData].sum()

            n = len(tot)

            x1 = tot.assign(Probabilidad=lambda x: x[simData]/suma)

            x2 = x1.sort_values(timeFrame)

            a = x2['Probabilidad']

            a1 = np.cumsum(a)

            x2['FPA'] = a1
            x2['Min'] = x2['FPA']
            x2['Max'] = x2['FPA']

            lis = x2["Min"].values
            lis2 = x2['Max'].values
            lis[0]= 0
            for i in range(1, len(lis2)):
                lis[i] = lis2[i-1]
            x2['Min'] = lis

            n, m, a, x0, c = int(qtty), 2**32, 22695477, 4, 1
            x = [1] * n
            r = [0.1] * n

            for i in range(0, n):
                x[i] = ((a*x0)+c) % m
                x0 = x[i]
                r[i] = round(x0 / m, 4)

            d = {'ri': r }
            dfMCL = pd.DataFrame(data=d)

            max = x2['Max'].to_list()
            min = x2['Min'].to_list()

            def search(arrmin, arrmax, value):
                for i in range (len(arrmin)):
                    if value >= arrmin[i] and value <= arrmax[i]:
                        return i
                return -1

            xpos = dfMCL['ri']
            posi = [0] * n

            for j in range(n):
                val = xpos[j]
                pos = search(min,max,val)
                posi[j] = pos

            x2['INDEX'] = x2.index.values
            x2 = x2.astype({'INDEX': 'int32'})
            x2.reset_index(drop = True)
            x2.set_index('INDEX', inplace = True, drop = False)

            simula = []
            for j in range(n):
                for i in range(n):
                    sim = x2.loc[x2['INDEX'] == posi[i]+1]
                    simu = sim.filter([simData]).values
                    iterator = itertools.chain(*simu)
                    for item in iterator:
                        a=item
                    simula.append(round(a, 2))

            dfMCL['Simulacion'] = pd.DataFrame(simula)

            index = []
            for i in range(len(dfMCL)):
                index.append(int(i))

            dfMCL['index'] = index

            dfMCL.set_index('index', inplace=True)

            resultsMod = dfModel.DataFrameModel(dfMCL)

            resultTableLabel = QLabel('Tabla de resultados')

            resultsTable = QTableView()
            resultsTable.setMinimumSize(750, 200)
            resultsTable.setMaximumSize(750, 200)
            resultsTable.setModel(resultsMod)

            vLayout = QVBoxLayout()
            vLayout.addWidget(resultTableLabel)
            vLayout.addWidget(resultsTable)
            
            vWidget = QWidget()
            vWidget.setLayout(vLayout)

            labelFileName = QLabel('Nombre del archivo (opcional): ')
            inputFileName = QLineEdit()

            btnSaveCsv = QPushButton('Guardar')
            btnSaveCsv.clicked.connect(lambda: self.saveCsv(df, inputFileName.text(), 'monte_carlo_'))

            hLayout = QHBoxLayout()
            hLayout.addWidget(labelFileName)
            hLayout.addWidget(inputFileName)
            hLayout.addWidget(btnSaveCsv)
            hWidget = QWidget()
            hWidget.setLayout(hLayout)

            self.vLayout.addWidget(vWidget, 1)
            self.vLayout.addWidget(hWidget, 1)
            self.vLayout.addStretch(1)

    def simInventarioInput(self): 

        index = self.vLayout.count()+1

        self.clearOutput(index)
        
        labelD = QLabel('Demanda (D): ')
        inputD = QLineEdit()

        labelCo = QLabel('Costo de ordenar (Co): ')
        inputCo = QLineEdit()

        labelCh = QLabel('Costo de mantenimiento (Ch): ')
        inputCh = QLineEdit()

        labelP = QLabel('Costo de producto (P): ')
        inputP = QLineEdit()

        labelTesp = QLabel('Tiempo de espera: ')
        inputTesp = QLineEdit()

        labelDias = QLabel('Días Año: ')
        inputDias = QLineEdit()

        labelStartI = QLabel('Inventario Inicial: ')
        inputStartI = QLineEdit()

        labelDemandD = QLabel('Distribución de demanda: ')
        demandDist = QComboBox()
        demandDist.addItem("Normal")
        demandDist.addItem("Triangular")
        demandDist.addItem("Constant")
        demandDist.resize(200, 50)

        labelTespD = QLabel('Distribución de tiempo de espera: ')
        inputTespD = QComboBox()
        inputTespD.addItem("Normal")
        inputTespD.addItem("Triangular")
        inputTespD.addItem("Constant")
        inputTespD.resize(200, 50)

        simBtn = QPushButton('Simular')
        simBtn.clicked.connect(lambda: self.simInventarioOutput(inputD.text(), inputCo.text(),
                                inputCh.text(), inputP.text(), inputTesp.text(), 
                                inputDias.text(), inputStartI.text(), demandDist.currentText(), 
                                inputTespD.currentText()))

        hLayout1 = QHBoxLayout()
        hLayout1.addWidget(labelD)
        hLayout1.addWidget(labelCo)
        hLayout1.addWidget(labelCh)
        h1 = QWidget()
        h1.setLayout(hLayout1)

        hLayout2 = QHBoxLayout()
        hLayout2.addWidget(inputD)
        hLayout2.addWidget(inputCo)
        hLayout2.addWidget(inputCh)
        h2 = QWidget()
        h2.setLayout(hLayout2)

        hLayout3 = QHBoxLayout()
        hLayout3.addWidget(labelP)
        hLayout3.addWidget(labelTesp)
        hLayout3.addWidget(labelDias)
        h3 = QWidget()
        h3.setLayout(hLayout3)

        hLayout4 = QHBoxLayout()
        hLayout4.addWidget(inputP)
        hLayout4.addWidget(inputTesp)
        hLayout4.addWidget(inputDias)
        h4 = QWidget()
        h4.setLayout(hLayout4)

        hLayout5 = QHBoxLayout()
        hLayout5.addWidget(labelStartI)
        hLayout5.addWidget(labelDemandD)
        hLayout5.addWidget(labelTespD)
        h5 = QWidget()
        h5.setLayout(hLayout5)

        hLayout6 = QHBoxLayout()
        hLayout6.addWidget(inputStartI, 1)
        hLayout6.addWidget(demandDist, 1)
        hLayout6.addWidget(inputTespD, 1)
        h6 = QWidget()
        h6.setLayout(hLayout6)

        hLayout7 = QHBoxLayout()
        hLayout7.addWidget(simBtn)
        h7 = QWidget()
        h7.setLayout(hLayout7)

        self.vLayout.addWidget(h1)
        self.vLayout.addWidget(h2)
        self.vLayout.addWidget(h3)
        self.vLayout.addWidget(h4)
        self.vLayout.addWidget(h5)
        self.vLayout.addWidget(h6)
        self.vLayout.addWidget(h7)
        self.vLayout.addStretch()

    def simInventarioOutput(self, D, Co, Ch, P, Tesp, Dias, startI, demndD, tespD):

        while True:
            try:
                D = float(D)
                Co = float(Co)
                Ch = float(Ch)
                P = float(P)
                Tesp = int(Tesp)
                Dias = int(Dias)
                startI = int(startI)

                Q = round(np.sqrt(((2*Co*D)/Ch)),2)
                N = round(D / Q,2)
                R = round((D / Dias) * Tesp,2)
                T = round(Dias / N,2)
                CoT = N * Co
                ChT = round(Q / 2 * Ch,2)
                MOQ = round(CoT + ChT,2)
                CTT = round(P * D + MOQ,2)

                indice = ['Q','Costo_ordenar','Costo_Mantenimiento','Costo_total','Diferencia_Costo_Total']

                periodo = np.arange(1, 19)

                def genera_lista(Q):

                    Q_Lista = []
                    i=1
                    Qi = Q
                    Q_Lista.append(Qi)
                    for i in range(1, 9):
                        Qi = Qi - 60
                        Q_Lista.append(Qi)

                    Qi = Q
                    for i in range(9, 18):
                        Qi = Qi + 60
                        Q_Lista.append(Qi)

                    return Q_Lista
                
                Lista = genera_lista(Q)
                Lista.sort()

                dfQ = pd.DataFrame(index=periodo, columns=indice).fillna(0)
                dfQ['Q'] = Lista

                for period in periodo:
                    dfQ['Costo_ordenar'][period] = float(D) * float(Co) / dfQ['Q'][period]
                    dfQ['Costo_Mantenimiento'][period] = dfQ['Q'][period] * Ch / 2
                    dfQ['Costo_total'][period] = dfQ['Costo_ordenar'][period] + dfQ['Costo_Mantenimiento'][period]
                    dfQ['Diferencia_Costo_Total'][period] = dfQ['Costo_total'][period] - MOQ

                def make_distribution(function,*pars):
                    def distribution():
                        return function(*pars)
                    return distribution

                def make_data(product, policy, periods):
                    """ Returns dataframe with the details of the inventory simulation.
                    Keyword arguments:
                    product -- Product object
                    policy -- dict that contains the policy name and parameters. For example:
                    policy = {'method': "Qs",
                    'param1': 20000,
                    'param2': 10000
                    }
                    periods -- numbers of periods of the simulation
                    """
                    periods += 1
                    # Create zero-filled Dataframe
                    period_lst = np.arange(periods) # index
                    # Abbreviations
                    # INV_INICIAL: INV_NETO_INICIALtial inventory position
                    # INV_NETO_INICIAL: INV_NETO_INICIALtial net inventory
                    # D: Demand
                    # INV_FINAL: Final inventory position
                    # INV_FINAL_NETO: Final net inventory
                    # LS: Lost sales
                    # AVG: Average inventory
                    # ORD: order quantity
                    # LT: lead time
                    header = ['INV_INICIAL','INV_NETO_INICIAL','DEMANDA', 'INV_FINAL',
                    'INV_FINAL_NETO', 'VENTAS_PERDIDAS', 'INV_PROMEDIO', 'CANT_ORDENAR', 'TIEMPO_LLEGADA']

                    df = pd.DataFrame(index=period_lst, columns=header).fillna(0)
                    # Create a list that will store each period order
                    order_l = [Order(quantity=0, lead_time=0)
                                for x in range(periods)]
                    # Fill DataFrame
                    for period in period_lst:
                        if period == 0:
                            df['INV_INICIAL'][period] = product.initial_inventory
                            df['INV_NETO_INICIAL'][period] = product.initial_inventory
                            df['INV_FINAL'][period] = product.initial_inventory
                            df['INV_FINAL_NETO'][period] = product.initial_inventory

                        if period >= 1:
                            df['INV_INICIAL'][period] = df['INV_FINAL'][period - 1] + order_l[period - 1].quantity
                            df['INV_NETO_INICIAL'][period] = df['INV_FINAL_NETO'][period - 1] + pending_order(order_l, period)
                            #demand = int(product.demand())

                            demand = 20
                            # We can't have negative demand

                            if demand > 0:
                                df['DEMANDA'][period] = demand
                            else:
                                df['DEMANDA'][period] = 0
                                # We can't have negative INV_INICIAL
                            if df['INV_INICIAL'][period] - df['DEMANDA'][period] < 0:
                                df['INV_FINAL'][period] = 0
                            else:
                                df['INV_FINAL'][period] = df['INV_INICIAL'][period] - df['DEMANDA'][period]
                                order_l[period].quantity, order_l[period].lead_time = placeorder(product,
                                df['INV_FINAL'][period], policy, period)
                                df['INV_FINAL_NETO'][period] = df['INV_NETO_INICIAL'][period] - df['DEMANDA'][period]
                            if df['INV_FINAL_NETO'][period] < 0:
                                df['VENTAS_PERDIDAS'][period] = abs(df['INV_FINAL_NETO'][period])
                                df['INV_FINAL_NETO'][period] = 0
                            else:
                                df['VENTAS_PERDIDAS'][period] = 0
                                df['INV_PROMEDIO'][period] = (df['INV_NETO_INICIAL'][period] 
                                + df['INV_FINAL_NETO'][period]) / 2.0
                                df['CANT_ORDENAR'][period] = order_l[period].quantity
                                df['TIEMPO_LLEGADA'][period] = order_l[period].lead_time
                    return df

                def pending_order(order_l, period):
                    """Return the order that arrives in actual period"""
                    indices = [i for i, order in enumerate(order_l) if order.quantity]
                    sum = 0
                    for i in indices:
                        if period - (i + order_l[i].lead_time + 1) == 0:
                            sum += order_l[i].quantity
                    return sum

                def demand(self):
                    if self.demand_dist == "Constant":
                        return self.demand_p1
                    elif self.demand_dist == "Normal":
                        return make_distribution(
                            np.random.normal,
                            self.demand_p1,
                            self.demand_p2
                        )()
                    elif self.demand_dist == "Triangular":
                        return make_distribution(
                            np.random_triangular,
                            self.demand_p1,
                            self.demand_p2,
                            self.demand_p3
                        )()
                        
                def lead_time(self):
                    if self.leadtime_dist == "Constant":
                        return self.leadtime_p1
                    elif self.leadtime_dist == "Normal":
                        return make_distribution(
                            np.random.normal,
                            self.leadtime_p1,
                            self.leadtime_p2
                        )()
                    if self.leadtime_dist == "Triangular":
                        return make_distribution(
                            np.random.triangular,
                                self.leadtime_p1,
                                self.leadtime_p2,
                                self.leadtime_p3
                            )()

                def __repr__(self):
                    return '<Product %r>' % self.name

                def placeorder(product, final_inv_pos, policy, period):
                    """Place the order according the inventory policy:
                    Keywords arguments:
                    product -- object Product
                    final_inv_pos -- final inventory position of period
                    policy -- chosen policy Qs or RS
                    period -- actual period
                    Return:
                    quantity to order
                    lead time
                    """
                    #lead_time = int(product.lead_time())
                    lead_time = 3
                    # Qs = if we hit the reorder point s, order Q units
                    if policy['method'] == 'Qs' and \
                        final_inv_pos <= policy['param2']:
                        return policy['param1'], lead_time
                    # RS = if we hit the review period R and the reorder point S, order: (S -
                    # final inventory pos)
                    elif policy['method'] == 'RS' and \
                        period % policy['param1'] == 0 and \
                            final_inv_pos <= policy['param2']:
                        return policy['param2'] - final_inv_pos, lead_time
                    else:
                        return 0, 0
                
                politica = {'method': "Qs",
                    'param1': 50,
                    'param2': 20
                }

                class Order(object):
                    """Object that stores basic data of an order"""
                    def __init__(self, quantity, lead_time):
                        self.quantity = quantity
                        self.lead_time = lead_time

                class product(object):
                    def __init__ (self,name,price,order_cost,initial_inventory,demand_dist,demand_p1,
                        demand_p2,demand_p3,leadtime_dist,leadtime_p1,leadtime_p2,leadtime_p3):
                        self.name=name
                        self.price=price
                        self.order_cost=order_cost
                        self.initial_inventory=initial_inventory
                        self.demand_dist=demand_dist
                        self.demand_p1=demand_p1
                        self.demand_p2=demand_p2
                        self.demand_p3=demand_p3
                        self.leadtime_dist=leadtime_dist
                        self.leadtime_p1=leadtime_p1
                        self.leadtime_p2=leadtime_p2
                        self.leadtime_p3=leadtime_p3

                producto = product("Producto", P, Co, startI, demndD, D, 0.0, 0.0, tespD, Tesp,0.0,
                0.0)
                df = make_data(producto, politica, 52)

                labelQ = QLabel("Cantidad Optima de Pedito Q: " + str(Q))
                labelCot = QLabel("Costo total de Ordenar CoT: " + str(CoT))
                labelCht = QLabel("Costo total de Mantener Inventario ChT =" + str(ChT))
                labelMOQ = QLabel("Costo Total de Ordenar y Mantener Inventario MO(O): " + str(MOQ))
                labelCTT = QLabel("Costo Total del Sistema de Inventario CTT: " + str(CTT))
                labelN = QLabel("Número total de pedidos: " + str(N))
                labelR = QLabel("Punto de reorden = R: " + str(R))
                labelT = QLabel("Tiempo de Pedido: " + str(T))

                model = dfModel.DataFrameModel(df)
                minCosTable = QTableView()
                minCosTable.setMinimumSize(750, 200)
                minCosTable.setMaximumSize(750, 200)
                minCosTable.setModel(model)

                figure = plt.figure(figsize=(12,8))
                plt.plot(dfQ.loc[:,'Costo_ordenar':'Costo_total'])
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
                btnSaveCsv.clicked.connect(lambda: self.saveCsv(df, inputFileName.text(), 'inventario_'))

                hLayout = QHBoxLayout()
                hLayout.addWidget(labelFileName)
                hLayout.addWidget(inputFileName)
                hLayout.addWidget(btnSaveCsv)
                hWidget = QWidget()
                hWidget.setLayout(hLayout)

                self.vLayout.addWidget(labelQ)
                self.vLayout.addWidget(labelCot)
                self.vLayout.addWidget(labelCht)
                self.vLayout.addWidget(labelMOQ)
                self.vLayout.addWidget(labelCTT)
                self.vLayout.addWidget(labelN)
                self.vLayout.addWidget(labelR)
                self.vLayout.addWidget(labelT)
                self.vLayout.addWidget(minCosTable)
                self.vLayout.addWidget(canvasElmt)
                self.addTableWithModel(df)
                self.vLayout.addWidget(hWidget)
                self.vLayout.addStretch()

                break
            except ValueError:
                dlg = QMessageBox(self)
                dlg.setWindowTitle('Error')
                dlg.setText('Ingrese solo números en los campos')
                dlg.setIcon(QMessageBox.Information)
                btn = dlg.exec()
                
                break

    def addTableWithModel(self, df):
        model = dfModel.DataFrameModel(df)
        table = QTableView()
        table.setMinimumSize(750, 200)
        table.setMaximumSize(750, 200)
        table.setModel(model)
        self.vLayout.addWidget(table)

    def simLineaEsperaInput(self):
        
        labelTasaMediaLl = QLabel('Tasa media de llegada: ')

        labelUnidades = QLabel('Unidades: ')
        inputUnidades = QLineEdit()

        labelTiempo = QLabel('Tiempo (minutos): ')
        inputTiempo = QLineEdit()

        labelTasaMediaServ = QLabel('Tasa media de servicio: ')
        inputTasaMediaServ = QLineEdit()

        labelUnidadesProb = QLabel('Unidades (Probabilidad): ')
        inputUnidadesProb = QLineEdit()

        labelQtty = QLabel('Cantidada de simulaciones: ')
        inputQtty = QLineEdit()

        btnSimular = QPushButton('Simular')
        btnSimular.clicked.connect(lambda: self.simLineaEsperaOutput(inputUnidades.text(), inputTiempo.text(),
                                    inputTasaMediaServ.text(), inputUnidadesProb.text(), inputQtty.text()))

        hLayout1 = QHBoxLayout()
        hLayout1.addWidget(labelUnidades)
        hLayout1.addWidget(inputUnidades)
        hLayout1.addWidget(labelTiempo)
        hLayout1.addWidget(inputTiempo)
        h1 = QWidget()
        h1.setLayout(hLayout1)
                
        hLayout2 = QHBoxLayout()
        hLayout2.addWidget(labelTasaMediaServ)
        hLayout2.addWidget(inputTasaMediaServ)
        hLayout2.addWidget(labelUnidadesProb)
        hLayout2.addWidget(inputUnidadesProb)
        h2 = QWidget()
        h2.setLayout(hLayout2)

        hLayout3 = QHBoxLayout()
        hLayout3.addWidget(labelQtty)
        hLayout3.addWidget(inputQtty)
        hLayout3.addWidget(btnSimular)
        h3 = QWidget()
        h3.setLayout(hLayout3)

        self.vLayout.addWidget(labelTasaMediaLl)
        self.vLayout.addWidget(h1)
        self.vLayout.addWidget(h2)
        self.vLayout.addWidget(h3)
        self.vLayout.addStretch()

    def simLineaEsperaOutput(self, u, t, s, n, qtty):

        if u.isdigit() and t.isdigit() and s.isdigit() and n.isdigit() and qtty.isdigit():
            landa = float(t)/float(u)
            nu = float(s)

            p = landa/nu
            Po = 1.0 - p
            Lq = landa**2/((nu-landa)*nu)
            L = landa/(nu-landa)
            W = 1/(nu-landa)
            Wq = W -(1.0/nu)
            Pn = p*int(n)*Po

            i = 0
            indice = ['ALL','ASE','TILL','TISE','TIRLL','TIISE','TIFSE','TIESP','TIESA']
            Clientes = np.arange(int(qtty))
            dfLE = pd.DataFrame(index=Clientes, columns=indice).fillna(0.000)
            np.random.seed(100)

            for i in Clientes:
                if i == 0:
                    dfLE['ALL'][i] = round(random.random(), 4)
                    dfLE['ASE'][i] = round(random.random(), 4)
                    dfLE['TILL'][i] = round(-1/landa*np.log(dfLE['ALL'][i]), 4)
                    dfLE['TISE'][i] = round(-1/nu*np.log(dfLE['ASE'][i]), 4)
                    dfLE['TIRLL'][i] = round(dfLE['TILL'][i], 4)
                    dfLE['TIISE'][i] = round(dfLE['TIRLL'][i], 4)
                    dfLE['TIFSE'][i] = round(dfLE['TIISE'][i] + dfLE['TISE'][i], 4)
                    dfLE['TIESA'][i] = round(dfLE['TIESP'][i] + dfLE['TISE'][i], 4)
                else:
                    dfLE['ALL'][i] = round(random.random(), 4)
                    dfLE['ASE'][i] = round(random.random(), 4)
                    dfLE['TILL'][i] = round(-1/landa*np.log(dfLE['ALL'][i]), 4)
                    dfLE['TISE'][i] = round(-1/nu*np.log(dfLE['ASE'][i]), 4)
                    dfLE['TIRLL'][i] = round(dfLE['TILL'][i] + dfLE['TIRLL'][i-1], 4)
                    dfLE['TIISE'][i] = round(max(dfLE['TIRLL'][i],dfLE['TIFSE'][i-1]), 4)
                    dfLE['TIFSE'][i] = round(dfLE['TIISE'][i] + dfLE['TISE'][i], 4)
                    dfLE['TIESP'][i] = round(dfLE['TIISE'][i] - dfLE['TIRLL'][i], 4)
                    dfLE['TIESA'][i] = round(dfLE['TIESP'][i] + dfLE['TISE'][i], 4)

            nuevas_columnas = pd.core.indexes.base.Index(["A_LLEGADA","A_SERVICIO","TIE_LLEGADA",
                        "TIE_SERVICIO","TIE_EXACTO_LLEGADA","TIE_INI_SERVICIO","TIE_FIN_SERVICIO",
                        "TIE_ESPERA","TIE_EN_SISTEMA"])

            dfLE.columns = nuevas_columnas

            tableModel = pdModel.pandasModel(dfLE)
            table = QTableView()
            table.setMinimumSize(750, 200)
            table.setMaximumSize(750, 200)
            table.setModel(tableModel)
            
            figure = plt.figure(figsize=(12,8))
            plt.plot(dfLE)
            canvas = FigureCanvasQTAgg(figure)
            toolbar = NavigationToolbar2QT(canvas, self)
            canvLayout = QVBoxLayout()
            canvLayout.addWidget(toolbar)
            canvLayout.addWidget(canvas)
            canvasElmt = QWidget()
            canvasElmt.setLayout(canvLayout)
            canvasElmt.setMinimumSize(300, 480)

            resultsModel = pdModel.pandasModel(dfLE.describe())
            resultsTable = QTableView()
            resultsTable.setMinimumSize(750, 200)
            resultsTable.setMaximumSize(750, 200)
            resultsTable.setModel(resultsModel)

            labelLanda = QLabel('Tasa media de llegada: ' + str(round(landa, 3)))
            labelNu = QLabel('Tasa media de servicio: ' + str(round(nu)))
            labelPo = QLabel('Probabilidad de que no haya unidades en el sistema: ' + str(round(Po, 3)))
            labelLq = QLabel('Promedio de unidades en linea de espera: ' + str(round(Lq, 3)))
            labelL = QLabel('Número esperado de clientes en el sistema: ' + str(round(L, 3)))
            labelWq = QLabel('Tiempo de espera en cola: ' + str(round(Wq, 3)))
            labelW = QLabel('Tiempo promedio que una unidad pasa en el sistema: ' + str(round(W, 3)))
            labelN = QLabel('Probabilidad que hayan ' + n + ' unidades en el sistema: ' + str(round(Pn, 3)))

            labelFileName = QLabel('Nombre del archivo')
            inputFileName = QLineEdit()

            btnSave = QPushButton('Guardar csv')
            btnSave.clicked.connect(lambda: self.saveCsv(dfLE.describe(), inputFileName.text(), 'linea_espera_'))

            hLayout = QHBoxLayout()
            hLayout.addWidget(labelFileName)
            hLayout.addWidget(inputFileName)
            hLayout.addWidget(btnSave)
            hW = QWidget()
            hW.setLayout(hLayout)

            self.vLayout.addWidget(labelLanda)
            self.vLayout.addWidget(labelNu)
            self.vLayout.addWidget(labelPo)
            self.vLayout.addWidget(labelLq)
            self.vLayout.addWidget(labelL)
            self.vLayout.addWidget(labelWq)
            self.vLayout.addWidget(labelW)
            self.vLayout.addWidget(labelN)
            self.vLayout.addWidget(table)
            self.vLayout.addWidget(canvasElmt)
            self.vLayout.addWidget(resultsTable)
            self.vLayout.addWidget(hW)

        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Error')
            dlg.setText('Ingrese solo números en los campos')
            dlg.setIcon(QMessageBox.Information)
            btn = dlg.exec()

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

    def clearOutput(self, index):
        
        for i in reversed(range(self.vLayout.count())): 
            if i > index:
                if self.vLayout.itemAt(i).widget() is not None:
                    self.vLayout.itemAt(i).widget().deleteLater()
                elif self.vLayout.itemAt(i).widget() is None:
                    self.vLayout.removeItem(self.vLayout.itemAt(i))

if __name__ == "__simulations__":
    
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Simulation()
    ui.show()
    sys.exit(app.exec_())
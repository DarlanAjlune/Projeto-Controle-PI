
from Utils.all import calcula_tudo, calcula_posterior
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import*
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import numpy as np
import random
import matplotlib.pyplot as plt
import os.path
import sqlite3

'''
    CONFIGURAÇÃO DO GRÁFICO
'''
class MplWidget(QWidget):
    
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        
        self.canvas = FigureCanvas(Figure())
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

'''
    CONFIGURAÇÃO DA JANELA PRINCIPAL
'''
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(749, 584)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = MplWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 40, 621, 361))
        self.widget.setObjectName("widget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 410, 621, 131))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(23)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(18, item)
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 621, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_ApplyStyle = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_ApplyStyle.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_ApplyStyle.setObjectName("horizontalLayout_ApplyStyle")
        self.pushButtonOpen = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButtonOpen.setObjectName("pushButtonOpen")
        self.horizontalLayout_ApplyStyle.addWidget(self.pushButtonOpen)
        self.notificationLabel = QtWidgets.QLabel(self.layoutWidget)
        self.notificationLabel.setText("")
        self.notificationLabel.setObjectName("notificationLabel")
        self.horizontalLayout_ApplyStyle.addWidget(self.notificationLabel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_ApplyStyle.addItem(spacerItem)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(640, 40, 101, 361))
        self.widget1.setObjectName("widget1")
        self.verticalLayoutInserir = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayoutInserir.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutInserir.setObjectName("verticalLayoutInserir")
        self.pushButtonInserir = QtWidgets.QPushButton(self.widget1)
        self.pushButtonInserir.setObjectName("pushButtonInserir")
        self.verticalLayoutInserir.addWidget(self.pushButtonInserir)
        self.tableWidgetInsert = QtWidgets.QTableWidget(self.widget1)
        self.tableWidgetInsert.setObjectName("tableWidgetInsert")
        self.tableWidgetInsert.setColumnCount(1)
        self.tableWidgetInsert.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetInsert.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetInsert.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetInsert.setHorizontalHeaderItem(0, item)
        self.verticalLayoutInserir.addWidget(self.tableWidgetInsert)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 749, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.flag = False

        # configuração toolbar
        self.toolbar = NavigationToolbar(self.widget.canvas, self.centralwidget)
        self.horizontalLayout_ApplyStyle.addWidget(self.toolbar)

        # configuração push button open
        self.pushButtonOpen.clicked.connect(self.getFile)
        # configuração botão insert
        self.pushButtonInserir.clicked.connect(self.getTableInsertData)

        # configuração tabela
        # setando colunas da tabela
        self.tableWidget.setColumnWidth(20,200)
        self.tableWidget.setColumnWidth(21,200)
        self.tableWidget.setColumnWidth(22,200)
        self.tableWidget.setColumnWidth(23,200)

        self.tableWidget.setHorizontalHeaderLabels(["ID","NOME_ARQUIVO","MP","TA","SP","KPLR","KILR","KPRF","KIRF","RiseTimeLR","OvershootLR","SettlingTimeLR","PeakLR"
        ,"PeakTimeLR","RiseTimeRF","OvershootRF","SettlingTimeRF","PeakRF","PeakTimeRF","PrecisaoOvershootLR","PrecisaoOvershootRF","PrecisaoSettlingTimeLR","PrecisaoSettlingTimeRF"])

    # método pega infos da tabela Insert
    def getTableInsertData(self):
        if self.flag:
            sp = float(self.tableWidgetInsert.item(0,0).text())
            kpRf = float(self.tableWidgetInsert.item(1,0).text())
            kiRf = float(self.tableWidgetInsert.item(2,0).text())
            kpLr = float(self.tableWidgetInsert.item(3,0).text())
            kiLr = float(self.tableWidgetInsert.item(4,0).text())
            self.update_graph_insert(sp,kpRf,kiRf,kpLr,kiLr)
        else:
            self.mp = float(self.tableWidgetInsert.item(0,0).text())
            self.ta = float(self.tableWidgetInsert.item(1,0).text())
            self.update_graph_import()

    # carrega infos do db na tabela inferior
    def load_data_db_table(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR + "\Database", "metadata_PI_controler.db")

        with sqlite3.connect(db_path) as db:
            cur = db.cursor()
            self.tableWidget.setRowCount(50)
            tablerow = 0
            sqlquery = "SELECT * FROM PI_CONTROLER"           
            # colocando dado Database --> Tablewidget
            for row in cur.execute(sqlquery):
                 self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                 self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                 self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                 self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                 self.tableWidget.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                 self.tableWidget.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                 self.tableWidget.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                 self.tableWidget.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(row[7])))
                 self.tableWidget.setItem(tablerow, 8, QtWidgets.QTableWidgetItem(str(row[8])))
                 self.tableWidget.setItem(tablerow, 9, QtWidgets.QTableWidgetItem(str(row[9])))
                 self.tableWidget.setItem(tablerow, 10, QtWidgets.QTableWidgetItem(str(row[10])))
                 self.tableWidget.setItem(tablerow, 11, QtWidgets.QTableWidgetItem(str(row[11])))
                 self.tableWidget.setItem(tablerow, 12, QtWidgets.QTableWidgetItem(str(row[12])))
                 self.tableWidget.setItem(tablerow, 13, QtWidgets.QTableWidgetItem(str(row[13])))
                 self.tableWidget.setItem(tablerow, 14, QtWidgets.QTableWidgetItem(str(row[14])))
                 self.tableWidget.setItem(tablerow, 15, QtWidgets.QTableWidgetItem(str(row[15])))
                 self.tableWidget.setItem(tablerow, 16, QtWidgets.QTableWidgetItem(str(row[16])))
                 self.tableWidget.setItem(tablerow, 17, QtWidgets.QTableWidgetItem(str(row[17])))
                 self.tableWidget.setItem(tablerow, 18, QtWidgets.QTableWidgetItem(str(row[18])))
                 tablerow+=1

    # operação INSERT no bd local
    def insert_data_db_table(self,sp,kpLR,kiLR,kpRF,kiRF,metadataLR,metadataRF):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR + "\Database", "metadata_PI_controler.db")

        # conecta com bd e insere dados
        with sqlite3.connect(db_path) as db:
            cur = db.cursor()
            cur.execute("insert into PI_CONTROLER values (?,?, ?, ?, ?, ?, ?, ? , ?,?,?,?,?,?,?,?,?,?,?)", (None,self.filename, float(self.mp), float(self.ta), float(sp), float(kpLR), float(kiLR), float(kpRF), float(kiRF), metadataLR[0], metadataLR[1], metadataLR[2], metadataLR[3], metadataLR[4], metadataRF[0], metadataRF[1], metadataRF[2], metadataRF[3], metadataRF[4]))

    # formatação da tabela insert
    def format_table_insert(self):
        if self.flag:
            for _ in range(2): self.tableWidgetInsert.removeRow(0)

            # add table 
            self.tableWidgetInsert.setRowCount(5)
            self.tableWidgetInsert.rowCount()

            #set table header
            self.tableWidgetInsert.setVerticalHeaderLabels(['sp','kpRf','kiRf','kpLr','kiLr'])

            # configuração tabela
            self.tableWidgetInsert.setColumnWidth(1,10)
        else:
            for _ in range(5): self.tableWidgetInsert.removeRow(0)

            # add table 
            self.tableWidgetInsert.setRowCount(2)
            self.tableWidgetInsert.rowCount()

            #set table header
            self.tableWidgetInsert.setVerticalHeaderLabels(['mp','ta'])

            # configuração tabela
            self.tableWidgetInsert.setColumnWidth(1,10)

    # método plot infos
    def update_graph_import(self):
            kpLR, kiLR, kpRF, kiRF,sp, t, rMF, rRF, rLR, rSMLR, rSMRF, rMA, metadataLR, metadataRF = calcula_tudo(self.mp,self.ta, self.filename)
            self.widget.canvas.axes.clear()
            self.widget.canvas.axes.plot(t,rMF,label='Resposta Malha Fechada')
            self.widget.canvas.axes.plot(t,rRF,label='Resposta Malha Fechada - RF - PI')
            self.widget.canvas.axes.plot(t,rLR,label='Resposta Malha Fechada - LR - PI')
            self.widget.canvas.axes.plot(t,rSMLR,label='Malha Fechada - LR - PI Ajustado')
            self.widget.canvas.axes.plot(t,rSMRF,label='Malha Fechada - RF - PI Ajustado')
            self.widget.canvas.axes.plot(t,rMA,label='Resposta Malha Aberta')
            self.widget.canvas.axes.legend(prop={'size':6},loc='upper right')
            self.widget.canvas.axes.set_title('Plot All')
            self.widget.canvas.axes.set_xlabel('Tempo [s]',fontsize=8)
            self.widget.canvas.axes.set_ylabel('Nível [cm]',fontsize=8)
            self.widget.canvas.draw()

            self.flag = True # mudança da tabela
            self.format_table_insert()
            self.insert_data_db_table(sp,kpLR,kiLR,kpRF,kiRF,metadataLR,metadataRF)
            self.load_data_db_table()

    # plot via dados tabela
    def update_graph_insert(self,sp,kpRF,kiRF,kpLR,kiLR):
            t, rSMFLR, rSMFRF, metadataLR, metadataRF = calcula_posterior(sp,kpRF,kiRF,kpLR,kiLR)
            self.widget.canvas.axes.clear()
            self.widget.canvas.axes.plot(t,rSMFLR,label='Malha Fechada - LR - PI Ajustado')
            self.widget.canvas.axes.plot(t,rSMFRF,label='Malha Fechada - RF - PI Ajustado')
            self.widget.canvas.axes.legend(prop={'size':6},loc='upper right')
            self.widget.canvas.axes.set_title('Plot All')
            self.widget.canvas.axes.set_xlabel('Tempo [s]',fontsize=8)
            self.widget.canvas.axes.set_ylabel('Nível [cm]',fontsize=8)
            self.insert_data_db_table(sp,kpLR,kiLR,kpRF,kiRF,metadataLR,metadataRF)

            self.widget.canvas.draw()

    # método get file .mat
    def getFile(self):
        '''
            Função que pega o endereço do arquivo .csv
            Também chama uma função read data
        '''
        self.flag = False
        self.filename = QFileDialog.getOpenFileName(filter="mat (*mat)")[0]
        print("File :", self.filename)
        self.notificationLabel.setText("OBS: inserir parâmetros obrigatórios")
        self.format_table_insert()

    # configs tabela
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PROJETO C213"))
        self.pushButtonOpen.setText(_translate("MainWindow", "Open"))
        self.pushButtonInserir.setText(_translate("MainWindow", "Inserir"))
        item = self.tableWidgetInsert.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "mp"))
        item = self.tableWidgetInsert.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "ta"))
        item = self.tableWidgetInsert.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "VALOR"))


# main
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-
"""
/***************************************************************************
          Cadastro de Mesas

        Autor      : Fabrício Rosa Amorim
        email      : fabricioamorimeac@hotmail.com
        Data       : 10/10/2010
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import sys
import os
import os.path
import csv

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

sys.path.append(r'C:\Users\fabri\Desktop\Teste1\Libs')
import psycopg2
from pyUFbr.baseuf import ufbr

# Carregando a interface
qtFile = r'C:\Users\fabri\Desktop\Teste1\mainwindow.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtFile)

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

#Definição de tarefas para seleção de processamento
        self.pushButton_2.clicked.connect(self.postgresql)
        self.radioButton_2.clicked.connect(self.toolboxBuscar)
        self.radioButton.clicked.connect(self.toolboxCadastro)
        self.radioButton_3.clicked.connect(self.toolboxCadastro)
        self.pushButton_4.clicked.connect(self.CadastroUsuario)
        #self.radioButton_2.clicked.connect(self.visualizarCadastros)
        self.pushButton.clicked.connect(self.visualizarCadastros)


#Inserção dos Estados do Brasil
        self.comboBox_1.currentIndexChanged.connect(self.Local)
        self.comboBox_1.clear()
        Estados = self.comboBox_1.addItems(ufbr.list_uf)

#Se selecionada a opção de busca, não exibe cadastro/login de usuário
    def toolboxBuscar(self):
        self.toolBox.setCurrentIndex(1)
    def toolboxCadastro(self):
        self.toolBox.setCurrentIndex(0)

#Inserção dos Municípios em acordo com o estado selecionado
    def Local(self):
        Estados = self.comboBox_1.currentText()
        self.comboBox_4.clear()
        cidadesPYUFBR = self.comboBox_4.addItems(ufbr.list_cidades(Estados))

#Criando a tabela de usuário no postgresql
    def CadastroUsuario(self):
        nomeUsuario	=	self.lineEdit.text()
        EnderecoUsuario	=	self.lineEdit_4.text()
        TipoUsuario	=	self.comboBox_9.currentText()
        CPF_CNPJ	=	self.lineEdit_9.text()
        Email	=	self.lineEdit_1.text()
        SenhaCodigo	=	self.lineEdit_3.text()

        if self.radioButton_4.isChecked():
#Verificando dados vazios
            if not nomeUsuario and EnderecoUsuario and CPF_CNPJ and Email and SenhaCodigo:
                self.label_11.setStyleSheet("color: red;")
                self.label_11.setText('Falha ao criar usuário, revise os dados de entrada')

            if nomeUsuario and EnderecoUsuario and CPF_CNPJ and Email and SenhaCodigo:
                con = psycopg2.connect(database = "CadastroPosicoes", user = "postgres", password = "Famorim007", host = "127.0.0.1", port = "5432")
                cur = con.cursor()
        #        database = cur.execute('''CREATE TABLE CadastroUsuario (nomeUsuario	VARCHAR (50), EnderecoUsuario	VARCHAR (50), TipoUsuario	VARCHAR (20), CPF_CNPJ	VARCHAR (20), Email	VARCHAR (50) PRIMARY KEY NOT NULL, SenhaCodigo	VARCHAR (50));''')
                cur.execute("SELECT Email, SenhaCodigo from CadastroUsuario")
                self.label_11.setStyleSheet("color: green;")
                self.label_11.setText('Usuário criado com sucesso')
                SQL = "INSERT INTO CadastroUsuario (nomeUsuario, EnderecoUsuario, TipoUsuario, CPF_CNPJ, Email, SenhaCodigo) VALUES  ('%s', '%s', '%s', '%s', '%s', '%s')" %  (nomeUsuario, EnderecoUsuario, TipoUsuario, CPF_CNPJ, Email, SenhaCodigo)
                cur.execute(SQL)
                con.commit()
                self.toolBox.setCurrentIndex(1)
#LOGIN USUARIO
        if self.radioButton_5.isChecked():
            con = psycopg2.connect(database = "CadastroPosicoes", user = "postgres", password = "Famorim007", host = "127.0.0.1", port = "5432")
            cur = con.cursor()
            cur.execute("SELECT Email, SenhaCodigo from CadastroUsuario")
            rows = cur.fetchall()
            for row in rows:
                if Email == row[0] and SenhaCodigo == row[1]:
                    self.label_11.setStyleSheet("color: green;")
                    self.label_11.setText('Acesso Permitido')
                    self.toolBox.setCurrentIndex(1)
                if Email != row[0] and SenhaCodigo != row[1]:
                    self.label_11.setStyleSheet("color: red;")
                    self.label_11.setText('Acesso negado, confira os dados de acesso')

#Implementação do Banco de Dados postgresql
    def postgresql(self):
            con = psycopg2.connect(database = "CadastroPosicoes", user = "postgres", password = "Famorim007", host = "127.0.0.1", port = "5432")
#Variáveis da interface
            Email	=	self.lineEdit_1.text()
            SenhaCodigo	=	self.lineEdit_3.text()
            DataInicio	=	self.dateEdit.date()
            HoraInicio	=	self.timeEdit.time()
            DataFinal	=	self.dateEdit_1.date()
            HoraFinal	=	self.timeEdit_1.time()
            EnderecoImovel	=	self.lineEdit_5.text()
            TipoImovel	=	self.comboBox_3.currentText()
            EstadoImovel	=	self.comboBox_1.currentText()
            CidadeImovel	=	self.comboBox_4.currentText()
            PontoReferencia	=	self.lineEdit_6.text()
            CEP	=	self.lineEdit_7.text()
            Bairro	=	self.lineEdit_8.text()
            Numero	=	self.spinBox.value()
            Descricao	=	self.lineEdit_2.text()
            Telefone	=	self.comboBox_5.currentText()
            Internet	=	self.comboBox_2.currentText()
            Mesas	=	self.comboBox_7.currentText()
            QtMesas	=	self.spinBox_2.value()
            Cadeiras	=	self.comboBox.currentText()
            QtCadeiras	=	self.spinBox_3.value()

#Criando a tabela de cadastro no postgresql
            cur = con.cursor()
            #database = cur.execute('''CREATE TABLE CadastroMesas (Email	VARCHAR (50) PRIMARY KEY NOT NULL, SenhaCodigo	VARCHAR (50), EnderecoImovel VARCHAR (50), TipoImovel CHAR (20), EstadoImovel	CHAR (20), CidadeImovel	CHAR (20), PontoReferencia	VARCHAR (100), CEP	VARCHAR (20), Bairro	VARCHAR (20), Numero	INT, Descricao	VARCHAR (100), Telefone	CHAR (10), Internet	CHAR (20), Mesas	CHAR (20), QtMesas	INT, Cadeiras	CHAR (20), QtCadeiras	INT);''')
            SQL = "INSERT INTO CadastroMesas (Email, SenhaCodigo, EnderecoImovel, TipoImovel, EstadoImovel, CidadeImovel, PontoReferencia, CEP, Bairro, Numero, Descricao, Telefone, Internet, Mesas, QtMesas, Cadeiras, QtCadeiras) VALUES  ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s', '%s', '%s', '%s', %s, '%s', %s)" % (Email, SenhaCodigo, EnderecoImovel, TipoImovel, EstadoImovel, CidadeImovel, PontoReferencia, CEP, Bairro, Numero, Descricao, Telefone, Internet, Mesas, QtMesas, Cadeiras, QtCadeiras)
            cur.execute(SQL)
            con.commit()
            self.label_11.setStyleSheet("color: green;")
            self.label_11.setText('Cadastro Armazenado')

    def visualizarCadastros(self):
        #Variáveis da interface
        Email	=	self.lineEdit_1.text()
        SenhaCodigo	=	self.lineEdit_3.text()
        DataInicio	=	self.dateEdit.date()
        HoraInicio	=	self.timeEdit.time()
        DataFinal	=	self.dateEdit_1.date()
        HoraFinal	=	self.timeEdit_1.time()
        EnderecoImovel	=	self.lineEdit_5.text()
        TipoImovel	=	self.comboBox_3.currentText()
        EstadoImovel	=	self.comboBox_1.currentText()
        CidadeImovel	=	self.comboBox_4.currentText()
        PontoReferencia	=	self.lineEdit_6.text()
        CEP	=	self.lineEdit_7.text()
        Bairro	=	self.lineEdit_8.text()
        Numero	=	self.spinBox.value()
        Descricao	=	self.lineEdit_2.text()
        Telefone	=	self.comboBox_5.currentText()
        Internet	=	self.comboBox_2.currentText()
        Mesas	=	self.comboBox_7.currentText()
        QtMesas	=	self.spinBox_2.value()
        Cadeiras	=	self.comboBox.currentText()
        QtCadeiras	=	self.spinBox_3.value()
        con = psycopg2.connect(database = "CadastroPosicoes", user = "postgres", password = "Famorim007", host = "127.0.0.1", port = "5432")
        cur = con.cursor()
        cur.execute("SELECT EnderecoImovel, TipoImovel, EstadoImovel, CidadeImovel, PontoReferencia, CEP, Bairro, Numero, Descricao, Telefone, Internet, Mesas, QtMesas, Cadeiras, QtCadeiras from CadastroMesas WHERE 'CidadeImovel' = 'ACRELÂNDIA'")
        rows = cur.fetchall()
        for row in rows:
            numcols = len(row[0])   # ( to get number of columns, count number of values in first row( first row is data[0]))
            numrows = len(row)   # (to get number of rows, count number of values(which are arrays) in data(2D array))
            self.tableWidget.setColumnCount(numcols)
            self.tableWidget.setRowCount(numrows)
            self.tableWidget.setItem(row, column, QTableWidgetItem((data[row][column])))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

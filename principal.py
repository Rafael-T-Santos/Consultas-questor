from PySide2.QtWidgets import (QApplication, QWidget, QLabel,
                               QLineEdit, QPushButton, QMessageBox, 
                               QFrame, QTableView, QHeaderView, QComboBox,
                               QDateEdit, QAbstractSpinBox, QAbstractItemView,
                               QTextEdit,QTableWidget )
from PySide2.QtGui import QIcon, QPixmap, QFont
from PySide2.QtCore import QDate, QSortFilterProxyModel

from datetime import date
from tkinter import Tk
from Models.modelo import CustomTableModel
from Models.modelo2 import CustomTableModel2
from Models.modelo3 import CustomTableModel3
from Models.modelo4 import CustomTableModel4
from datetime import date, datetime

import Controllers.banco as b
import sys
import pyperclip as pc

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Assistente de Consultas - QUESTOR")
        global altura_monitor, largura_monitor
        altura_monitor = Tk().winfo_screenheight()
        largura_monitor = Tk().winfo_screenwidth()

        # x,y,w,h -> Afastado da esquerda, afastado do topo, largura, altura
        self.setGeometry(largura_monitor*0.1, altura_monitor*0.1, largura_monitor*0.8, altura_monitor*0.8)
        self.setAutoFillBackground(True)
        self.setStyleSheet('background-color: #aecfca;')

        self.set_icon()
        self.def_formulario()

    def set_icon(self):
        appIcon = QIcon("imgs/logo.png")
        self.setWindowIcon(appIcon)

    def def_formulario(self):
        altura_view = altura_monitor*0.8 - 90
        largura_view = largura_monitor*0.8 - 210

        font_btn = QFont("fonts/Exo2_Bold.ttf", 14)
        self.btn_cadastrar = QPushButton('Cadastrar', self)
        self.btn_cadastrar.setFont(font_btn)
        self.btn_cadastrar.setGeometry(0, 0, 170, 50)
        self.btn_cadastrar.clicked.connect(self.frame_cadastrar)

        self.btn_pesquisar = QPushButton('Pesquisar', self)
        self.btn_pesquisar.setFont(font_btn)
        self.btn_pesquisar.setGeometry(0, 50, 170, 50)
        self.btn_pesquisar.clicked.connect(self.frame_pesquisar)

        self.btn_relatorio = QPushButton('Relatorio Estoque', self)
        self.btn_relatorio.setFont(font_btn)
        self.btn_relatorio.setGeometry(0, 100, 170, 50)
        self.btn_relatorio.clicked.connect(self.frame_relatorio)

        self.btn_relatorio_fcp = QPushButton('Relatorios Geral', self)
        self.btn_relatorio_fcp.setFont(font_btn)
        self.btn_relatorio_fcp.setGeometry(0, 150, 170, 50)
        self.btn_relatorio_fcp.clicked.connect(self.frame_relatorio_fcp)

        self.btn_relatorio_fcp = QPushButton('E-mails Notas', self)
        self.btn_relatorio_fcp.setFont(font_btn)
        self.btn_relatorio_fcp.setGeometry(0, 200, 170, 50)
        self.btn_relatorio_fcp.clicked.connect(self.frame_email)

        '''
        FRAME DE CADASTRO ===============================================================================
        '''
        global frm_cadastrar
        self.frm_cadastrar = QFrame(self)
        self.frm_cadastrar.setGeometry(170, 0, 1920, 1080)
        self.frm_cadastrar.setStyleSheet('background-color: #cde4e0')
        self.frm_cadastrar.setVisible(False)

        self.lbl_nome = QLabel('Nome Consulta:', self.frm_cadastrar)
        self.lbl_nome.setGeometry(20, 20, 110, 22)

        self.lbl_sql = QLabel('SQL', self.frm_cadastrar)
        self.lbl_sql.setGeometry(20, 44, 100, 22)

        self.txt_nome = QLineEdit(self.frm_cadastrar)
        self.txt_nome.setGeometry(120, 20, 200, 22)

        self.txt_sql = QTextEdit(self.frm_cadastrar)
        self.txt_sql.setGeometry(20, 70, largura_view, altura_view)
        self.txt_sql.setStyleSheet('background-color: #D5ece9')

        self.btn_limpar = QPushButton('Gravar', self.frm_cadastrar)
        self.btn_limpar.setGeometry(330, 20, 110, 22)

        self.btn_gravar = QPushButton('Limpar', self.frm_cadastrar)
        self.btn_gravar.setGeometry(450, 20, 110, 22)

        '''
        FRAME DE CONSULTA SQL ===============================================================================
        '''
        global frm_pesquisar
        self.frm_pesquisar = QFrame(self)
        self.frm_pesquisar.setGeometry(170, 0, 1920, 1080)
        self.frm_pesquisar.setStyleSheet('background-color: #cde4e0')
        self.frm_pesquisar.setVisible(False)

        self.lbl_cod = QLabel('SQL:', self.frm_pesquisar)
        self.lbl_cod.setGeometry(20, 20, 55, 16)

        global txt_cod_pesquisa
        self.txt_cod_pesquisa = QLineEdit(self.frm_pesquisar)
        self.txt_cod_pesquisa.setGeometry(80, 20, 600, 22)

        self.tabela_consulta = QTableView(self.frm_pesquisar)
        self.tabela_consulta.setGeometry(20, 70, largura_view, altura_view)
        self.tabela_consulta.verticalHeader().setVisible(False)
        self.tabela_consulta.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela_consulta.setFrameShape(QFrame.WinPanel)
        self.tabela_consulta.setSortingEnabled(True)

        self.btn_pesquisar = QPushButton('Consultar', self.frm_pesquisar)
        self.btn_pesquisar.setGeometry(700, 20, 80, 22)
        self.btn_pesquisar.clicked.connect(self.consulta_personalizada)

        '''
        FRAME DE RELATORIO ESTOQUE ============================================================================
        '''
        global frm_relatorio
        self.frm_relatorio = QFrame(self)
        self.frm_relatorio.setGeometry(170, 0, 1920, 1080)
        self.frm_relatorio.setStyleSheet('background-color: #cde4e0')
        self.frm_relatorio.setVisible(False)

        self.lbl_cod = QLabel('Cód.', self.frm_relatorio)
        self.lbl_cod.setGeometry(20, 20, 55, 22)

        global txt_cod_consulta
        self.txt_cod_consulta = QLineEdit(self.frm_relatorio)
        self.txt_cod_consulta.setGeometry(80, 20, 200, 22)

        self.btn_pesquisar = QPushButton('Pesquisar', self.frm_relatorio)
        self.btn_pesquisar.setGeometry(300, 20, 80, 22)
        self.btn_pesquisar.clicked.connect(self.consulta_produtos)

        self.btn_limpar = QPushButton('Limpar', self.frm_relatorio)
        self.btn_limpar.setGeometry(400, 20, 80, 22)
        self.btn_limpar.clicked.connect(self.limpa_relatorio)

        self.tabela = QTableView(self.frm_relatorio)
        self.tabela.setGeometry(20, 70, largura_view, altura_view)
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela.setFrameShape(QFrame.WinPanel)
        self.tabela.setSortingEnabled(True)

        self.titulos = self.tabela.horizontalHeader()
        self.titulos.setSectionResizeMode(QHeaderView.ResizeToContents)

        '''
        FRAME DE RELATORIOS QUE NÃO PRECISAM DE VARIAVEL =========================================================================
        '''
        global frm_relatorio_fcp
        global combo_box

        self.frm_relatorio_fcp = QFrame(self)
        self.frm_relatorio_fcp.setGeometry(170, 0, 1920, 1080)
        self.frm_relatorio_fcp.setStyleSheet('background-color: #cde4e0')
        self.frm_relatorio_fcp.setVisible(False)

        self.lbl_cod = QLabel('Relatório', self.frm_relatorio_fcp)
        self.lbl_cod.setGeometry(20, 20, 80, 22)

        self.combo_box = QComboBox(self.frm_relatorio_fcp)
        self.combo_box.setGeometry(80, 20, 200, 22)
        self.combo_box.setStyleSheet('background-color: white')
        self.lista_combo_box = ['Produtos sem Fecoep', 'Faturamento em CPF','Retiradas Pendentes']
        self.combo_box.addItems(self.lista_combo_box)

        self.btn_pesquisar = QPushButton('Pesquisar', self.frm_relatorio_fcp)
        self.btn_pesquisar.setGeometry(300, 20, 80, 22)
        self.btn_pesquisar.clicked.connect(self.print_relatorio)

        self.btn_limpar = QPushButton('Limpar', self.frm_relatorio_fcp)
        self.btn_limpar.setGeometry(400, 20, 80, 22)
        self.btn_limpar.clicked.connect(self.limpa_fecoep)

        self.tabela_fcp = QTableView(self.frm_relatorio_fcp)
        self.tabela_fcp.setGeometry(20, 70, largura_view, altura_view)
        self.tabela_fcp.verticalHeader().setVisible(False)
        self.tabela_fcp.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela_fcp.setFrameShape(QFrame.WinPanel)
        self.tabela_fcp.setSortingEnabled(True)

        self.titulos = self.tabela_fcp.horizontalHeader()

        '''
        FRAME DE RELATORIO PARA ENVIAR EMAIL ============================================================================
        '''
 
        global frm_email
        global data_faturamento

        self.frm_email = QFrame(self)
        self.frm_email.setGeometry(170, 0, 1920, 1080)
        self.frm_email.setStyleSheet('background-color: #cde4e0')
        self.frm_email.setVisible(False)

        self.lbl_cod = QLabel('Data de Faturamento:', self.frm_email)
        self.lbl_cod.setGeometry(20, 20, 110, 22)

        self.data_faturamento = QDateEdit(self.frm_email)
        self.data_faturamento.setGeometry(140, 20, 100, 22)
        self.data_faturamento.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.data_faturamento.setCalendarPopup(True)
        today = date.today()
        hoje = today.strftime("%Y,%m,%d")
        ano_mes_dia = hoje.split(",")
        ano = int(ano_mes_dia[0])
        mes = ano_mes_dia[1]
        mes = mes.replace('0','')
        mes = int(mes)
        dia = int(ano_mes_dia[2])
        self.data_faturamento.setDate(QDate(ano,mes,dia))

        self.txt_resultado_email = QLineEdit(self.frm_email)
        self.txt_resultado_email.setGeometry(20,44,largura_view,22)
        self.txt_resultado_email.setReadOnly(True)   

        self.tabela_email = QTableView(self.frm_email)
        self.tabela_email.setGeometry(20, 70, largura_view, altura_view)
        self.tabela_email.verticalHeader().setVisible(False)
        self.tabela_email.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela_email.setFrameShape(QFrame.WinPanel)
        self.tabela_email.setSortingEnabled(True)

        self.titulos = self.tabela_email.horizontalHeader()
        self.titulos.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.btn_pesquisar = QPushButton('Consultar', self.frm_email)
        self.btn_pesquisar.setGeometry(300, 20, 80, 22)
        self.btn_pesquisar.clicked.connect(self.consulta_email_faturado)

        self.btn_copiar = QPushButton('Copiar', self.frm_email)
        self.btn_copiar.setGeometry(400, 20, 60, 22)
        self.btn_copiar.clicked.connect(self.copiar_txt_resultado_email)

        self.btn_limpar = QPushButton('Limpar', self.frm_email)
        self.btn_limpar.setGeometry(480, 20, 80, 22)
        self.btn_limpar.clicked.connect(self.limpa_email)
        

        global meus_frames
        self.meus_frames = (self.frm_cadastrar, self.frm_pesquisar,
                            self.frm_relatorio, self.frm_relatorio_fcp,
                            self.frm_email)

    def copiar_txt_resultado_email(self):
        copia = self.txt_resultado_email.text()
        pc.copy(copia)

    def print_relatorio(self):
        self.limpa_fecoep()
        valor_combo_box = self.combo_box.currentText()
        if valor_combo_box == 'Produtos sem Fecoep':
            self.consulta_fecoep()
        elif valor_combo_box == 'Faturamento em CPF':
            self.faturamento_cpf()
        elif valor_combo_box == 'Retiradas Pendentes':
            self.consulta_retiradas()

    def consulta_produtos(self):
        global txt_cod_consulta
        produtos = self.txt_cod_consulta.text()
        produtos = produtos.replace(';',',')
        dados = b.consulta_produtos(produtos)
        self.modelo = CustomTableModel(dados)

        proxymodel = QSortFilterProxyModel()
        proxymodel.setSourceModel(self.modelo)

        self.tabela.setModel(proxymodel)

    def consulta_fecoep(self):
        dados = b.consulta_fecoep()
        self.modelo = CustomTableModel2(dados)
        
        proxymodel = QSortFilterProxyModel()
        proxymodel.setSourceModel(self.modelo)

        self.tabela_fcp.setModel(proxymodel)

    def faturamento_cpf(self):
        dados = b.faturamento_cpf()
        self.modelo = CustomTableModel3(dados)

        proxymodel = QSortFilterProxyModel()
        proxymodel.setSourceModel(self.modelo)

        self.tabela_fcp.setModel(proxymodel)

    def consulta_retiradas(self):
        dados = b.consulta_retiradas()
        self.modelo = CustomTableModel3(dados)

        proxymodel = QSortFilterProxyModel()
        proxymodel.setSourceModel(self.modelo)

        self.tabela_fcp.setModel(proxymodel)

    def consulta_personalizada(self):
        sql_personalizado = self.txt_cod_pesquisa.text()
        dados = b.consulta_personalizada(sql_personalizado)
        self.modelo = CustomTableModel3(dados)

        proxymodel = QSortFilterProxyModel()
        proxymodel.setSourceModel(self.modelo)

        self.tabela_consulta.setModel(proxymodel)

    def consulta_email_faturado(self):
        global data_faturamento
        data = str(self.data_faturamento.date())
        data = data.replace('PySide2.QtCore.QDate(', '').replace(')', '').replace(', ','-')
        data = datetime.strptime(data, '%Y-%m-%d').date()

        dados = b.consulta_faturadas_email(data)
        self.modelo = CustomTableModel4(dados)

        proxymodel = QSortFilterProxyModel()
        proxymodel.setSourceModel(self.modelo)

        self.tabela_email.setModel(proxymodel)
        dados2 = list(dados[0])

        lista = []

        for i in range(len(dados2)):
            lista.append(dados2[i][0])
        lista = str(lista).replace('[','').replace(']','')
        lista = "1 or cd_cliente in ("+lista+")"
        self.txt_resultado_email.setText(lista)             

    def ocultar_frames(self):
        global meus_frames
        for f in self.meus_frames:
            if f.isVisible() == True:
                f.setVisible(False)

    def frame_cadastrar(self):
        global frm_cadastrar
        self.ocultar_frames()
        self.frm_cadastrar.setVisible(True)

    def frame_pesquisar(self):
        global frm_pesquisar
        self.ocultar_frames()
        self.tabela_consulta.setModel(None)
        self.frm_pesquisar.setVisible(True)

    def frame_relatorio(self):
        global frm_relatorio
        self.ocultar_frames()
        self.tabela.setModel(None)
        self.frm_relatorio.setVisible(True)

    def frame_relatorio_fcp(self):
        global frm_relatorio_fcp
        self.ocultar_frames()
        self.tabela_fcp.setModel(None)
        self.frm_relatorio_fcp.setVisible(True)

    def frame_email(self):
        global frm_email
        self.ocultar_frames()
        self.tabela_email.setModel(None)
        self.frm_email.setVisible(True)
        self.txt_resultado_email.setText("")

    def limpa_fecoep(self):
        global frm_relatorio_fcp
        self.tabela_fcp.setModel(None)

    def limpa_relatorio(self):
        global frm_relatorio
        self.tabela.setModel(None)

    def limpa_email(self):
        global frm_email
        self.tabela_email.setModel(None)
        self.txt_resultado_email.setText("")


def executa():
    myApp = QApplication.instance()

    if myApp is None:
        myApp = QApplication(sys.argv)

    janela = Window()
    janela.show()
    myApp.exec_()

#executa()

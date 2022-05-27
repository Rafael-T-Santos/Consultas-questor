from telnetlib import LOGOUT
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide2.QtGui import QIcon, QPixmap, QFont
from PySide2 import QtCore
import sys
import Controllers.controle as c

class Window(QWidget):
    global logou, tentativas
    logou = False
    tentativas = 0

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Assistente de Consultas - QUESTOR")
        self.setFixedSize(800, 450)
        self.setToolTip("Janela de Login")
        self.setAutoFillBackground(True)
        self.setStyleSheet('background-color: white;')

        self.fundo_direito()
        self.set_icon()
        self.set_img()
        self.set_form()
        self.set_btn()

    def set_icon(self):
        appIcon = QIcon("imgs/logo.png")
        self.setWindowIcon(appIcon)

    def fundo_direito(self):
        fundo = QLabel('', self)
        fundo.setGeometry(400, 0, 400, 450)
        fundo.setStyleSheet('background-color:#81CAB2;')

    def set_img(self):
        icon_img = QIcon("imgs/logo.jpg")
        lbl_img = QLabel('Olá', self)
        lbl_img.move(475, 75)
        pixmap_img = icon_img.pixmap(300, 300, QIcon.Active)
        lbl_img.setPixmap(pixmap_img)

    def set_form(self):
        global campo_user, campo_senha

        font_title = QFont("fonts/Exo2_Bold.ttf", 14)
        font_campos = QFont("fonts/Exo2_VariableFont_wght.ttf", 11)

        lbl_title = QLabel('Bem Vindo', self)
        lbl_title.setGeometry(100, 50, 300, 100)
        lbl_title.setFont(font_title)

        lbl_user = QLabel('Usuário', self)
        lbl_user.move(100, 150)
        lbl_user.setFont(font_campos)

        campo_user = QLineEdit(self)
        campo_user.move(100, 170)
        campo_user.setFont(font_campos)

        lbl_senha = QLabel('Senha', self)
        lbl_senha.move(100, 210)
        lbl_senha.setFont(font_campos)

        campo_senha = QLineEdit(self)
        campo_senha.move(100, 230)
        campo_senha.setFont(font_campos)
        # campo_senha.setPlaceholderText('Digite sua senha') #Caso quisesse que esse texto ficasse dentro do quadro da senha
        campo_senha.setEchoMode(QLineEdit.EchoMode.Password)
        campo_senha.returnPressed.connect(self.validar_login)

    def set_btn(self):
        global btn_entrar

        font_btn = QFont("fonts/Exo2_VariableFont_wght.ttf", 11)
        btn_entrar = QPushButton('Entrar', self)
        btn_entrar.move(100, 270)
        btn_entrar.clicked.connect(self.validar_login)
        btn_entrar.setFont(font_btn)
        btn_entrar.setStyleSheet('background-color:#81CAB2;')

        btn_sair = QPushButton('Sair', self)
        btn_sair.move(190, 270)
        btn_sair.clicked.connect(self.btn_sair)
        btn_sair.setFont(font_btn)
        btn_sair.setStyleSheet('background-color:#81CAB2;')

    def btn_sair(self):
        info = QMessageBox.question(self,
                                    'Assistente de Consultas',
                                    'Deseja fechar o sistema ?',
                                    QMessageBox.Yes | QMessageBox.No)
        if info == QMessageBox.Yes:
            sys.exit(0)
        else:
            pass

    def validar_login(self):
        global tentativas, logou

        us = campo_user.text()
        us = us.upper()
        pw = campo_senha.text()

        if c.validar_usuario(us, pw):
            logou = True
            self.close()
        else:
            if tentativas < 3:
                msg = QMessageBox()
                appIcon = QIcon("imgs/logo.png")
                msg.setWindowIcon(appIcon)
                msg.setText('Usuário ou senha inválido!')
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle('Assistente de Consultas')
                msg.exec()
                tentativas += 1
            else:
                msg2 = QMessageBox()
                appIcon = QIcon("imgs/logo.png")
                msg2.setWindowIcon(appIcon)
                msg2.setIcon(QMessageBox.Critical)
                msg2.setWindowTitle('Assistente de Consultas')
                msg2.setText('Número de tentativas esgotou. \nO Sistema será fechado.')
                msg2.exec()
                sys.exit(0)


def executa():
    global logou
    myApp = QApplication.instance()

    if myApp is None:
        myApp = QApplication(sys.argv)

    janela = Window()
    janela.show()
    myApp.exec_()
    return logou

#executa()
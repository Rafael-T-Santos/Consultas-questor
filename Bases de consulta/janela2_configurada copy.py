# QApplication é a aplicação em si, e QWidgets são as coisas dentro da janela
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide2.QtGui import QIcon, QPixmap, QFont
import sys


# Classe que constroi a janela


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Assistente de Consultas QUESTOR")
        # x,y,w,h -> Afastado da esquerda, afastado do topo, largura, algura
        self.setGeometry(300, 200, 800, 600)
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.setMaximumWidth(800)
        self.setMaximumHeight(600)
        self.setToolTip("Janela de Login")
        self.setAutoFillBackground(True)
        self.setStyleSheet('background-color: lightblue')

        self.set_icon()
        self.set_img()
        self.set_form()
        self.set_btn()

    def set_icon(self):
        appIcon = QIcon("imgs/logo.png")
        self.setWindowIcon(appIcon)

    def set_img(self):
        # Imagem direita
        icon_img = QIcon("imgs/logo.png")
        lbl_img = QLabel('Olá', self)
        lbl_img.move(450, 150)
        pixmap_img = icon_img.pixmap(300, 300, QIcon.Active)
        lbl_img.setPixmap(pixmap_img)

    def set_form(self):
        font_title = QFont("fonts/Exo2_Bold.ttf", 14)
        font_campos = QFont("fonts/Exo2_VariableFont_wght.ttf", 11)
        # Msg Bem Vindo
        lbl_title = QLabel(
            'Bem Vindo \nInforme seus dados para entrar no sistema', self)
        lbl_title.move(50, 50)
        lbl_title.setFont(font_title)

        lbl_user = QLabel('Usuário', self)
        lbl_user.move(50, 150)
        lbl_user.setFont(font_campos)

        campo_user = QLineEdit(self)
        campo_user.move(50, 170)
        campo_user.setFont(font_campos)

        lbl_senha = QLabel('Senha', self)
        lbl_senha.move(50, 210)
        lbl_senha.setFont(font_campos)

        campo_senha = QLineEdit(self)
        campo_senha.move(50, 230)
        campo_senha.setFont(font_campos)
        # campo_senha.setPlaceholderText('Digite sua senha') #Caso quisesse que esse texto ficasse dentro do quadro da senha
        campo_senha.setEchoMode(QLineEdit.EchoMode.Password)

    def set_btn(self):
        btn_entrar = QPushButton('Entrar', self)
        btn_entrar.move(50, 270)
        # quando o botão for clicado, se conecta a uma função e a executa
        btn_entrar.clicked.connect(self.btn_entrar)

        btn_sair = QPushButton('Sair', self)
        btn_sair.move(50, 310)
        btn_sair.clicked.connect(self.btn_sair)

    def btn_entrar(self):
        info = QMessageBox.about(
            self, 'Assistente de Consultas', 'Clicou Entrar')

    def btn_sair(self):
        info = QMessageBox.question(self,
                                    'Assistente de Consultas',
                                    'Deseja fechar o sistema ?',
                                    QMessageBox.Yes | QMessageBox.No)
        if info == QMessageBox.Yes:
            sys.exit()
        else:
            pass


myApp = QApplication(sys.argv)

janela = Window()
janela.show()

myApp.exec_()
sys.exit(0)

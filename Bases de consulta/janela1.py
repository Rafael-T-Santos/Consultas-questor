from PySide2.QtWidgets import QApplication, QWidget
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()


myApp = QApplication(sys.argv)

janela = Window()
janela.show()

myApp.exec_()
sys.exit(0)
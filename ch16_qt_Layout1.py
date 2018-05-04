# 잘못된 레이아웃의 예시


import sys
from PyQt5.QtWidgets import *

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(600, 200, 1200, 600)


        self.textEdit = QTextEdit(self)
        self.textEdit.resize(280, 250)
        self.textEdit.move(10, 10)

        self.pushButton = QPushButton('저장', self)
        self.pushButton.resize(280, 25)
        self.pushButton.move(10, 270)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow =MyWindow()
    mywindow.show()
    app.exec_()
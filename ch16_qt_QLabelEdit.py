import sys
from PyQt5.QtWidgets import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 400, 300, 150)

        # Label
        label = QLabel("종목 코드", self)
        label.move(20, 20)

        # Line Edit
        self.lineEdit = QLineEdit("", self)
        self.lineEdit.move(20, 20)
        self.lineEdit.textChanged.connect(self.lineEditChanged)

        # Status Bar
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def lineEditChanged(self):
        self.statusBar.showMessage(self.lineEdit.text())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_() # _이 있는 것은 pyqt4, python2에서는 이렇게 써야해서 이전버전의 호환을 위해서 이렇게 사용한다.


import sys

from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *


# class definition - 모든 일이 이루어지는 곳. OCX객체 생성
class MyWindow(QMainWindow):
    def __init__(self):
        # pass : 함수 안에 아무것도 안할때는 반드시 pass를 입력해줘야한다.
        super().__init__()  # 상위클래스 불러올때 사용하는것
        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 150)

        # QAxWidget 은 QWidget과 QAxBase를 상속한다.
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        btn1 = QPushButton("login", self)
        btn1.move(20, 20)
        btn1.clicked.connect(self.btn1_clicked)

        btn2 = QPushButton("Check state", self)
        btn2.move(20, 70)
        btn2.clicked.connect(self.btn2_clicked)

        # signal-slot 처리
        # 버튼 클릭 및 로그인 처리

    def btn1_clicked(self):
        ret = self.kiwoom.dynamicCall("CommConnect()")

    def btn2_clicked(self):
        if self.kiwoom.dynamicCall("GetConnectState()") == 0:
            self.statusBar().showMessage("Not connected")
        else:
            self.statusBar().showMessage("Connected")


# entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()  # 객체 생성
    myWindow.show()  # 화면에 나타나게끔 하는 것
    app.exec_()  # 이벤트 루프 실행

import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *


class Kiwoom(QAxWidget):  # Kiwoom 클래스에서는 QAxWidget 클래스를 상속받음으로써 Kiwoom 클래스의 인스턴스가 QAxWidget 클래스가 제공하는 메서드를 호출할 수 있다
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    def _create_kiwoom_instance(self):  # 메서드의 이름에 언더스코어(_)를 붙여준 것은 _create_kiwoom_instance라는 메서드가 주로 Kiwoom 클래스의 메서드에서 호출되기 때문
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):  # 연결 되었는가 안되었는가
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()

    def get_code_list_by_market(self, market): # GetCodeListByMarket 메서드를 호출하는 용도
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';') # ; 을 기준으로 split
        return code_list[:-1]

    def get_master_code_name(self, code):  # 한글 종목명을 얻어오는 메서드
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name


if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    # Get CodeList
    code_list = kiwoom.get_code_list_by_market('10')
    for code in code_list:
        print(code, end=" ")
    print()
    # Get MasterCodeName
    print(kiwoom.get_master_code_name("000660"))



import sys
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication

TR_REQ_TIME_INTERVAL = 0.2


class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    def _create_kiwoom_instance(self):
        self.setControl('KHOPENAPI.KHOpenAPICtrl.1')

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)
        self.OnReceiveChejanData.connect(self._receive_chejan_data)

    def comm_connect(self):
        self.dynamicCall('CommConnect()')
        self._login_event_loop = QEventLoop()
        self._login_event_loop.exec()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("Connected")
        else:
            print("Disconnected")

        self._login_event_loop.exit()

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall('GetCodeListByMarket(QString)', market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall('GetMasterCodeName(QString)', code)
        return code_name

    def get_connect_state(self):
        ret = self.dynamicCall('GetConnectState()')
        return ret

    def set_input_value(self, id, value):
        self.dynamicCall('SetInputValue(QString, QString)', id, value)

    def comm_rq_data(self, rq_name, tr_code, prev_next, screen_no):
        self.dynamicCall('CommRqData(QString, QString, int, QString)',
                         rq_name, tr_code, prev_next, screen_no)
        self._tr_event_loop = QEventLoop()
        self._tr_event_loop.exec()

    def _get_comm_data(self, tr_code, record_name, index, item_name):
        ret = self.dynamicCall('GetCommData(QString, QString, int, QString)',
                               tr_code, record_name, index, item_name)
        return ret

    def _comm_get_data(self, tr_code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", tr_code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, tr_code, record_name):
        ret = self.dynamicCall('GetRepeatCnt(QString, QString)',
                               tr_code, record_name)
        return ret

    def _receive_tr_data(self, scr_no, rq_name, tr_code, record_name, pre_next,
                         unused1, unused2, unused3, unused4):
        ret = {'scr_no': scr_no, 'rq_name': rq_name, 'tr_code': tr_code,
               'record_name': record_name, 'pre_next': pre_next}


        if pre_next == '2':
            self.data_remained = True
        else:
            self.data_remained = False

        if rq_name == "opt10081_req":
            self._opt10081(rq_name, tr_code)
        elif rq_name == "opw00001_req":
            self._opw00001(rq_name, tr_code)
        elif rq_name == "opw00018_req":
            self._opw00018(rq_name, tr_code)

        try:
            self._tr_event_loop.exit()
        except AttributeError:
            pass

    def _opt10081(self, rq_name, tr_code):
        data_cnt = self._get_repeat_cnt(tr_code, rq_name)

        for i in range(data_cnt):
            date = self._get_comm_data(tr_code, rq_name, i, '일자')
            open = self._get_comm_data(tr_code, rq_name, i, '시가')
            high = self._get_comm_data(tr_code, rq_name, i, '고가')
            low = self._get_comm_data(tr_code, rq_name, i, '저가')
            close = self._get_comm_data(tr_code, rq_name, i, '현재가')
            volume = self._get_comm_data(tr_code, rq_name, i, '거래량')

            self.ohlcv['date'].append(date)
            self.ohlcv['open'].append(int(open))
            self.ohlcv['high'].append(int(high))
            self.ohlcv['low'].append(int(low))
            self.ohlcv['close'].append(int(close))
            self.ohlcv['volume'].append(int(volume))

    def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                         [rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no])

    def get_chejan_data(self, fid):
        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret

    def get_login_info(self, tag):
        ret = self.dynamicCall("GetLoginInfo(QString)", tag)
        return ret

    def _receive_chejan_data(self, gubun, item_cnt, fid_list):
        print(gubun)
        print(self.get_chejan_data(9203))
        print(self.get_chejan_data(302))
        print(self.get_chejan_data(900))
        print(self.get_chejan_data(901))

    def _opw00001(self, rqname, trcode):
        d2_deposit = self._get_comm_data(trcode, rqname, 0, "d+2추정예수금")
        self.d2_deposit = Kiwoom.change_format(d2_deposit)

    @staticmethod
    def change_format(data):
        strip_data = data.lstrip('-0')  # - 나 0 이 있으면 모두 지워라!  lstrip(문자의 모음)
        if strip_data == '' or strip_data == '.00':
            strip_data = '0'

        format_data = format(int(strip_data), 'd')  # strip_data를 정수형으로 바꾸고, 1000 자리 마다 ,를 찍어준다.
        if data.startswith('-'):
            format_data = '-' + format_data

        return format_data

    @staticmethod
    def change_format2(data):  # 수익률에 대한 포맷 변경
        strip_data = data.lstrip('-0')

        if strip_data == '':
            strip_data = '0'

        if strip_data.startswith('.'):  # .이 있는 경우를 따진다. 소수점 이하 첫째자리로 끝나는 경우도 처리한다.
            strip_data = '0' + strip_data

        if data.startswith('-'):
            strip_data = '-' + strip_data

        return strip_data

    def _opw00018(self, rqname, trcode):
        # single data
        total_purchase_price = self._get_comm_data(trcode, rqname, 0, "총매입금액")
        total_eval_price = self._get_comm_data(trcode, rqname, 0, "총평가금액")
        total_eval_profit_loss_price = self._get_comm_data(trcode, rqname, 0, "총평가손익금액")
        total_earning_rate = self._get_comm_data(trcode, rqname, 0, "총수익률(%)")
        estimated_deposit = self._get_comm_data(trcode, rqname, 0, "추정예탁자산")

        # total_earning_rate = Kiwoom.change_format(total_earning_rate)
        # print('모의투자서버?', self.get_server_gubun())  # 모의 투자 서버라면?
        # if self.get_server_gubun():
        #     total_earning_rate = float(total_earning_rate) / 100
        #     total_earning_rate = str(total_earning_rate)

        self.opw00018_output['single'].append(Kiwoom.change_format(total_purchase_price))
        self.opw00018_output['single'].append(Kiwoom.change_format(total_eval_price))
        self.opw00018_output['single'].append(Kiwoom.change_format(total_eval_profit_loss_price))
        self.opw00018_output['single'].append(Kiwoom.change_format2(total_earning_rate))  # 비율이니까 소수점까지 처리하는 포맷2로!
        self.opw00018_output['single'].append(Kiwoom.change_format(estimated_deposit))

        # multi data
        rows = self._get_repeat_cnt(trcode, rqname)
        for i in range(rows):
            name = self._get_comm_data(trcode, rqname, i, "종목명")
            quantity = self._get_comm_data(trcode, rqname, i, "보유수량")
            purchase_price = self._get_comm_data(trcode, rqname, i, "매입가")
            current_price = self._get_comm_data(trcode, rqname, i, "현재가")
            eval_profit_loss_price = self._get_comm_data(trcode,  rqname, i, "평가손익")
            earning_rate = self._get_comm_data(trcode, rqname, i, "수익률(%)")

            quantity = Kiwoom.change_format(quantity)
            purchase_price = Kiwoom.change_format(purchase_price)
            current_price = Kiwoom.change_format(current_price)
            eval_profit_loss_price = Kiwoom.change_format(eval_profit_loss_price)
            earning_rate = Kiwoom.change_format2(earning_rate)

            self.opw00018_output['multi'].append([name, quantity, purchase_price, current_price,
                                                  eval_profit_loss_price, earning_rate])

    def reset_opw00018_output(self):  # 사전
        self.opw00018_output = {'single': [], 'multi': []}

    def get_server_gubun(self): # 서버를 구분지어보자
        ret = self.dynamicCall("KOA_Functions(QString, QString)", "GetServerGubun", "")
        return ret


if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()
    kiwoom.reset_opw00018_output()

    account_number = kiwoom.get_login_info("ACCNO")
    account_number = account_number.split(';')[0]

    kiwoom.set_input_value("계좌번호", account_number)
    kiwoom.comm_rq_data("opw00018_req", "opw00018", 0, "2000")

    kiwoom.set_input_value("계좌번호", account_number)
    kiwoom.comm_rq_data("opw00018_req", "opw00018", 0, "2000")

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
import time
import sqlite3
import pandas as pd

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

    def comm_connect(self):
        self.dynamicCall('CommConnect()')
        self._login_event_loop = QEventLoop()
        self._login_event_loop.exec()

    def _event_connect(self, err_code):
        if err_code == 0:
            print('Connected!')
        else:
            print('Not Connected!')

        self._login_event_loop.exit()

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall('GetCodeListByMarket(QString)', market)
        return code_list.split(';')[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall('GetMasterCodeName(QString)', code)
        return code_name

    def set_input_value(self, id, value):
        self.dynamicCall('SetInputValue(QString, QString)', id, value)

    def comm_rq_data(self, rq_name, tr_code, prev_next, screen_no):
        self.dynamicCall('CommRqData(QString, QString, int, QString)', rq_name, tr_code, prev_next, screen_no)

        self._tr_event_loop = QEventLoop()
        self._tr_event_loop.exec()

    def _get_comm_data(self, tr_code, rq_name, index, item_name):
        ret = self.dynamicCall('GetCommData(QString, QString, int, QString', tr_code, rq_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, tr_code, rq_name):
        ret = self.dynamicCall('GetRepeatCnt(QString, QString)', tr_code, rq_name)
        return ret

    def _receive_tr_data(self, scr_no, rq_name, tr_code, record_name, prev_next, unused1, unused2, unused3, unused4):
        if prev_next == '2':
            self.data_remained = True
        else:
            self.data_remained = False

        if rq_name == 'opt10081_req':
            self._opt10081(rq_name, tr_code)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()
    kiwoom.ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}

    # opt10081 TR 요청
    kiwoom.set_input_value('종목코드', '035720')  # 카카오
    kiwoom.set_input_value('기준일자', '20180504')
    kiwoom.set_input_value('수정주가구분', '1')
    kiwoom.comm_rq_data('opt10081_req', 'opt10081', 0, '0101')

    while kiwoom.data_remained:
        print('fetching...')
        time.sleep(TR_REQ_TIME_INTERVAL)
        kiwoom.set_input_value('종목코드', '035720')
        kiwoom.set_input_value('기준일자', '20180504')
        kiwoom.set_input_value('수정주가구분', '1')
        kiwoom.comm_rq_data('opt10081_req', 'opt10081', 2, '0101')

    df = pd.DataFrame(kiwoom.ohlcv,
                      columns=['open', 'high', 'low', 'close', 'volume'],
                      index=kiwoom.ohlcv['date'])

    con = sqlite3.connect('D:\DEV64\dev_python\Trading\PyTrader\stock.db')
    df.to_sql('035720', con, if_exists='replace')
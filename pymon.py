import datetime
import sys
import time

from PyQt5.QtWidgets import *
import Kiwoom
from pandas import DataFrame

TR_REQ_TIME_INTERVAL = 0.5
MARKET_KOSPI   = 0
MARKET_KOSDAQ  = 10

class PyMon:
    def __init__(self):
        self.kiwoom = Kiwoom.Kiwoom()
        self.kiwoom.comm_connect()
        self.get_code_list()

    def get_code_list(self):
        self.kospi_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSPI)
        self.kosdaq_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSDAQ)

    # 오늘 날짜를 시작으로 과거 거래일별로 시가, 고가, 저가, 종가, 거래량을 가져오는 메서드
    def get_ohlcv(self, code, start):
        self.kiwoom.ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}

        self.kiwoom.set_input_value("종목코드", code)
        self.kiwoom.set_input_value("기준일자", start)
        self.kiwoom.set_input_value("수정주가구분", 1)
        self.kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")
        time.sleep(0.2)

        df = DataFrame(self.kiwoom.ohlcv, columns=['open', 'high', 'low', 'close', 'volume'],
                       index=self.kiwoom.ohlcv['date'])
        return df

    # 급등주 포착하는 알고리즘
    def check_speedy_rising_volume(self, code):
        today = datetime.datetime.today().strftime("%Y%m%d")
        df = self.get_ohlcv(code, today)
        volumes = df['volume']

    # 조회 시작일을 기준으로 이전 20일간 거래량의 평균을 계산해야 하므로
    # 총 21일 치의 데이터가 필요합니다. 만약 최근에 상장된 종목이라면 데이터가
    # 충분하지 않을 수 있으므로 이 경우에는if 문을 사용해 걸러냈습니다.
    #  check_speedy_rising_volume 메서드는 해당 종목이 거래량 기준 급등주인 경우
    # True를 반환하고 급등주가 아닌 경우에는 False를 반환합니다.
    # 따라서 데이터가 충분하지 않은 종목에 대해서는 False를 반환합니다.

        if len(volumes) < 21:
            return False

        sum_vol20 = 0
        today_vol = 0

        for i, vol in enumerate(volumes):
            if i == 0:
                today_vol = vol
            elif 1 <= i <= 20:
                sum_vol20 += vol
            else:
                break

        avg_vol20 = sum_vol20 / 20
        if today_vol > avg_vol20 * 10:
            return True

    def run(self):
        num = len(self.kosdaq_codes)

        for i, code in enumerate(self.kosdaq_codes):
            print(i, '/', num)
            if self.check_speedy_rising_volume(code):
                print("급등주: ", code)
            time.sleep(TR_REQ_TIME_INTERVAL)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    pymon = PyMon()
    pymon.run()
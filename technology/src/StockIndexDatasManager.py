
import tushare as ts
import pandas as pd
from stock_analysis.auxiliary_lib.NounsEng2Chn import NounsEng2Chn
import stock_analysis.auxiliary_lib.util as util

'''
    获取所有的指数信息
'''
class StockIndexDatasManager:
    __pro = None
    __basic_path:str = "../datas/指数数据"
    __index_dict = None   # 保存指数代码，重点（000001、399001、399005、399006）
    def __init__(self):
        util.deletePath(self.__basic_path)
        util.createPath(self.__basic_path)
        self.__index_dict = {
            '上证指数': '000001.sh',
            '深证成指': '399001.sz',
            '中小板指': '399005.zxb',
            '创业板指': '399006.cyb'
            # '沪深300': '000300.hs300',
            # '上证50': '000016.sz50'
        }

    def setPro(self, pro):
        self.__pro = pro

    '''
    获取交易指数的基本信息
    重点：
        上证指数
        深证成指
        创业板指
    '''
    def getAllIndexDaily(self):
        with pd.ExcelWriter(r"../datas/指数数据/指数日K.xlsx") as xlsx:
            for name, code in self.__index_dict.items():
                if code != '000001.sh':     # 先做上证指数分析
                    continue
                df_SpecIndex = self.__pro.index_daily(ts_code=code, start_date='20200101')
                df_SpecIndex = df_SpecIndex.reset_index()
                df_SpecIndex = NounsEng2Chn().converseEng2Chn(df_SpecIndex, NounsEng2Chn.mDataSpecIndexTradingDaily)
                df_SpecIndex.to_excel(xlsx, sheet_name=name, index=False)
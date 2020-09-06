
'''
    股票基本接口测试程序
'''

import tushare as ts
from auxiliary_lib.NounsEng2Chn import NounsEng2Chn
from pandas import DataFrame
import pandas as pd

## 初始化tushare token(基本接口用不到)    <class 'tushare.pro.client.DataApi'>
# pro = tushare.pro_api(token='063c3e42ec30996bf395ddb0b7875918b2280544dee0c7e657b8136d')

'''
    获取所有股票的当日数据
'''
def getAllStockTradingDayData():
    df_AllStock = ts.get_today_all()
    df_AllStock = NounsEng2Chn().converseEng2Chn(df_AllStock, NounsEng2Chn().mDataTradingDaysMap)
    df_AllStock.to_excel("../datas/股票数据/股票实时数据.xlsx", sheet_name='股票实时信息')

'''
    获取指定股票历史数据
'''
def getSpecStockTest():
    code = "000001"
    df_SpecStockHistory = ts.get_hist_data(code, start='2020-01-01')
    df_SpecStockHistory = NounsEng2Chn().converseEng2Chn(df_SpecStockHistory, NounsEng2Chn.mDataSpecStockHistory)
    df_SpecStockHistory.to_excel("../datas/" + code + "历史数据.xlsx", sheet_name='股票历史信息')

'''
    查询当前所有正常上市交易的股票列表
'''
def getAllStockInfo():
    df_StockInfo = ts.get_stock_basics()
    df_StockInfo = NounsEng2Chn().converseEng2Chn(df_StockInfo, NounsEng2Chn.mDataCompanyBasicInfo)
    df_StockInfo.to_excel("../datas/股票数据/当前上市交易的股票列表.xlsx", sheet_name='股票列表')

'''
    新接口：查询当前所有正常上市交易的股票列表
'''
def getAllStockInfoPro():
    pro = ts.pro_api(token='e5ccd9b1da858f2e127afef26431dd550ebd8d837f2394816722f0f9')
    df_StockInfo = pro.stock_basic()
    # df_StockInfo = NounsEng2Chn().converseEng2Chn(df_StockInfo, NounsEng2Chn.mDataCompanyBasicInfo)
    df_StockInfo.to_excel("../datas/股票数据/当前上市交易的股票列表.xlsx", sheet_name='股票列表')

if __name__ == '__main__':
    # getAllStockTradingDayData()
    getSpecStockTest()
    # getAllStockInfo()
    # getAllStockInfoPro()
    pass
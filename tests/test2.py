
import tushare as ts
import numpy as np
from stock_analysis.auxiliary_lib.NounsEng2Chn import NounsEng2Chn

pro = ts.pro_api(token='063c3e42ec30996bf395ddb0b7875918b2280544dee0c7e657b8136d')

'''
    获取交易指数的基本信息
    重点：
        上证指数
        深证成指
        创业板指
    链接：
        https://www.imooc.com/article/282866
'''
def getAllIndexTest():
    df_IndexInfo = ts.get_index()
    df_IndexInfo = NounsEng2Chn().converseEng2Chn(df_IndexInfo, NounsEng2Chn.mDataAllIndexInfo)
    df_IndexInfo.to_excel("../datas/指数数据/交易指数基本信息.xlsx", sheet_name='交易指数')

'''
    获取特定交易所下的指数信息
    重点：
        全球指数：MSCI
        上交所指数：SSE
        深交所指数：SZSE
'''
def getSpecIndexTest():
    df_IndexInfo = pro.index_basic(market='SW')
    df_IndexInfo = NounsEng2Chn().converseEng2Chn(df_IndexInfo, NounsEng2Chn.mDataSpecIndexInfo)
    df_IndexInfo.to_excel("../datas/指数数据/上证指数.xlsx", sheet_name='指数行情')

def getSpecIndexHistory():
    # 获取常见股票指数行情，通过 pro.index_daily 接口
    indexs = {
        '上证指数': '000001.sh',
        '深证成指': '399001.sz',
        '中小板指': '399005.zxb',
        '创业板指': '399006.cyb',
        '沪深300': '000300.hs300',
        '上证50': '000016.sz50'
    }

    # def_SpecIndex = ts.get_hist_data('sh', start='2019-01-01')    # 旧接口

    # df_SpecIndex = pro.index_daily(ts_code='000001.sh')
    # 或者按日期取
    df_SpecIndex = pro.index_daily(ts_code='000001.sh', start_date='20200101', end_date='20200801')
    df_SpecIndex = NounsEng2Chn().converseEng2Chn(df_SpecIndex, NounsEng2Chn.mDataSpecIndexTradingDaily)
    df_SpecIndex.to_excel("../datas/指数数据/上证指数.xlsx", sheet_name='指数行情')

if __name__ == '__main__':
    # getAllIndexTest()
    # getSpecIndexTest()
    getSpecIndexHistory()
    pass
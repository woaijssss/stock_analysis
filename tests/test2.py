
import tushare as ts
from stock_analysis.auxiliary_lib.NounsEng2Chn import NounsEng2Chn

pro = ts.pro_api(token='063c3e42ec30996bf395ddb0b7875918b2280544dee0c7e657b8136d')

'''
    获取交易指数的基本信息
    重点：
        上证指数
        深证成指
        创业板指
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

if __name__ == '__main__':
    # getAllIndexTest()
    # getSpecIndexTest()
    pass
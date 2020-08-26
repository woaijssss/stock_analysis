
import tushare as ts
from stock_analysis.auxiliary_lib.NounsEng2Chn import NounsEng2Chn
import stock_analysis.auxiliary_lib.util as util

'''
    获取所有的指数信息
'''
class StockIndexDatasManager:
    __pro = None
    __basic_path:str = "../datas/指数数据"
    __index_list = []   # 保存指数代码，重点（000001、399001、399005、399006）
    def __init__(self):
        util.deletePath(self.__basic_path)
        util.createPath(self.__basic_path)

    def setPro(self, pro):
        self.__pro = pro

    '''
    获取交易指数的基本信息
    重点：
        上证指数
        深证成指
        创业板指
    '''
    def getAllIndexInfo(self):
        df_IndexInfo = ts.get_index()
        df_IndexInfo = NounsEng2Chn().converseEng2Chn(df_IndexInfo, NounsEng2Chn.mDataAllIndexInfo)
        df_IndexInfo.to_excel(self.__basic_path + "/交易指数基本信息.xlsx", sheet_name='交易指数')
        __index_list = list(df_IndexInfo["指数代码"])
        print(__index_list)
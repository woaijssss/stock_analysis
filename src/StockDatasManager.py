
import tushare as ts
from stock_analysis.auxiliary_lib.NounsEng2Chn import NounsEng2Chn
import stock_analysis.auxiliary_lib.util as util

class StockDatasManager:
    __pro = None
    __basic_path:str = "../datas/股票数据"
    __stock_code_list = []      # 保存所有股票代码(不含科创板)
    __stock_ts_code_list = []

    def __init__(self):
        util.deletePath(self.__basic_path)
        util.createPath(self.__basic_path)

    def setPro(self, pro):
        self.__pro = pro

    '''
        查询当前所有正常上市交易的股票列表
    '''
    def getAllStockInfo(self):
        df_StockInfo = ts.get_stock_basics()
        df_StockInfo = df_StockInfo.reset_index()
        df_StockInfo = NounsEng2Chn().converseEng2Chn(df_StockInfo, NounsEng2Chn.mDataCompanyBasicInfo)
        df_StockInfo.to_excel("../datas/股票数据/当前上市交易的股票列表.xlsx", sheet_name='股票列表', index=False)

    '''
        新接口：查询当前所有正常上市交易的股票列表
    '''
    def getAllStockInfoPro(self):
        df_StockInfo = self.__pro.stock_basic()
        df_StockInfo = df_StockInfo.reset_index()
        df_StockInfo = NounsEng2Chn().converseEng2Chn(df_StockInfo, NounsEng2Chn.mDataAllStockBasicInfo)
        df_StockInfo.to_excel("../datas/A_当前上市交易的股票列表.xlsx", sheet_name='股票列表', index=False)
        # __stock_code_list = list(df_StockInfo["code"])
        for i in range(0, len(df_StockInfo)):
            df_line = df_StockInfo.iloc[i]
            if df_line["市场类型（主板/中小板/创业板/科创板）"] != '科创板':
                self.__stock_code_list.append(df_line["股票代码"])
                self.__stock_ts_code_list.append(df_line["TS代码"])

    '''
        获取所有股票的历史数据
            从 20200101 开始
    '''
    def getAllStockHistoryDatas(self):
        for code in self.__stock_code_list:
            df_SpecStockHistory = ts.get_hist_data(code, start='2020-01-01')
            if df_SpecStockHistory is None:
                print("None: ", code)
                continue
            df_SpecStockHistory = df_SpecStockHistory.reset_index()
            df_SpecStockHistory = NounsEng2Chn().converseEng2Chn(df_SpecStockHistory, NounsEng2Chn.mDataSpecStockHistory)
            df_SpecStockHistory.to_excel("../datas/股票数据/" + code + "历史数据.xlsx", sheet_name='历史日K数据', index=False)

import tushare as ts
from auxiliary_lib.NounsEng2Chn import NounsEng2Chn
from auxiliary_lib.ConfigLoader import ConfigLoader
import auxiliary_lib.util as util
from src.analysis_department.StockAnalyst import StockAnalyst
import time


class StockDatasManager:
    __pro = None
    __basic_path: str = "../datas/股票数据"
    __stock_code_map = {}  # 保存所有股票代码-股票名称对照关系(不含科创板)
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
        NounsEng2Chn().converseStockCode2Chn(df_StockInfo)
        df_StockInfo.to_excel("../datas/A_当前上市交易的股票列表.xlsx", sheet_name='股票列表', index=False)
        # __stock_code_list = list(df_StockInfo["code"])
        for i in range(0, len(df_StockInfo)):
            df_line = df_StockInfo.iloc[i]
            name = df_line["股票名称"]
            if df_line["市场类型（主板/中小板/创业板/科创板）"] != '科创板' and "ST" not in name:
                code = df_line["股票代码"]
                self.__stock_code_map[code] = name
                self.__stock_ts_code_list.append(df_line["TS代码"])

    '''
        获取所有股票的历史数据
            从 20200101 开始
    '''

    def getAllStockHistoryDatas(self):
        count = 0
        length = len(self.__stock_code_map)
        code_list_cfg = ConfigLoader().get("stocks", "code_list")

        startDate = ConfigLoader().get("stocks", "history_data_start_date")
        if startDate == '-1':
            sevenDaySecs = 60 * 60 * 24 * 7
            now = time.time()
            date = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(now - sevenDaySecs))
            startDate = date.split('T')[0]
        print('起始日期： ' + startDate)

        for code, name in self.__stock_code_map.items():
            count += 1
            if code_list_cfg and code not in code_list_cfg:
                continue

            df_SpecStockHistory = ts.get_hist_data(code, start=startDate)
            if df_SpecStockHistory is None:
                print("None: ", code)
                continue
            StockAnalyst().setCode2Name(code, name)
            print("第 %d 支股票: [%s]，共 %d 支" % (count, StockAnalyst().getNameByCode(code), length))
            df_SpecStockHistory = df_SpecStockHistory.reset_index()
            df_SpecStockHistory = NounsEng2Chn().converseEng2Chn(df_SpecStockHistory,
                                                                 NounsEng2Chn.mDataSpecStockHistory)
            filename = code + NounsEng2Chn().mStockCode2Chn.get(code) + ".xlsx"
            df_SpecStockHistory.to_excel("../datas/股票数据/" + filename, sheet_name='历史日K数据', index=False)

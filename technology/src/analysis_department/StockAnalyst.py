import pandas as pd
from pandas import DataFrame
from src.stock_forms.StockKLineFormChecker import StockKLineFormChecker

'''
    股票数据分析器
'''


class StockAnalyst(object):
    __root_path = "../datas/股票数据/"
    __stockMap = None
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.__stockMap = {
            "000524": "岭南控股",
            "002108": "沧州明珠",
            "002138": "顺络电子",
            "002407": "多氟多",
            "002625": "光启技术",
            "600776": "东方通信",
            "603703": "盛洋科技",
            "603869": "新智认知"
        }

    def startAnalysis(self):
        for id in self.__stockMap.keys():
            df = pd.read_excel(self.__root_path + id + self.__stockMap[id] + '.xlsx', sheet_name='历史日K数据',
                               parse_dates=True)
            print('-----------------------------: ' + id + self.__stockMap[id])
            oneDay_res = self.oneDayAnalysisIndicators(df)
            twoDay_res = self.twoDayAnalysisIndicators(df)
            threeDay_res = self.threeDayAnalysisIndicators(df)
            if oneDay_res or twoDay_res or threeDay_res:
                print('K线分析结论： 可操作')
            else:
                print('K线分析结论： 不可操作！！！！')
            print('===========================================\n')


    ########################################################################################################################
    def oneDayAnalysisIndicators(self, df: DataFrame):
        resList = []
        for i in range(0, 7):
            line_lst = list(df.iloc[i])
            date, open, high, close, low = line_lst[0:5]
            day = [open, high, close, low]
            if StockKLineFormChecker().checkSingleKLineForm(day):
                resList.append(date)
        print("一天的指标： ", resList)
        if len(resList):
            return True
        return False


    def twoDayAnalysisIndicators(self, df: DataFrame):
        resList = []
        for i in range(0, 7):
            dayOne = list(df.iloc[i + 1])
            dayTwo = list(df.iloc[i])
            if StockKLineFormChecker().checkDoubleKLineForm(dayOne, dayTwo):
                resList.append(dayOne[0])
        print("两天的指标： ", resList)
        if len(resList):
            return True
        return False


    def threeDayAnalysisIndicators(self, df: DataFrame):
        resList = []
        for i in range(0, 7):
            dayOne = list(df.iloc[i + 2])
            dayTwo = list(df.iloc[i + 1])
            dayThree = list(df.iloc[i])
            if StockKLineFormChecker().checkMultipleKLineForm(dayOne, dayTwo, dayThree):
                resList.append(dayTwo[0])
        print("三天的指标： ", resList)
        if len(resList):
            return True
        return False

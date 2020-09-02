import pandas as pd
from pandas import DataFrame
from src.stock_forms.StockKLineFormChecker import StockKLineFormChecker
from auxiliary_lib.ConfigLoader import ConfigLoader

'''
    股票数据分析器
'''


class StockAnalyst(object):
    __root_path = "../datas/股票数据/"
    __stockMap = None
    __instance = None
    __analysis_days = int(ConfigLoader().get("stocks", "analysis_days"))

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
            "603869": "新智认知",
            "600988": "赤峰黄金"
        }

    def startAnalysis(self):
        columns = ["股票代码", "股票名称", "一天形态", "两天形态", "多天形态", "操作决策"]
        df_result = DataFrame(columns=columns)
        for id in self.__stockMap.keys():
            df = pd.read_excel(self.__root_path + id + self.__stockMap[id] + '.xlsx', sheet_name='历史日K数据',
                               parse_dates=True)
            print('-----------------------------: ' + id + self.__stockMap[id])
            oneDay_res = self.oneDayAnalysisIndicators(df)
            twoDay_res = self.twoDayAnalysisIndicators(df)
            threeDay_res = self.threeDayAnalysisIndicators(df)
            # print("一天: " + oneDay_res)
            # print("二天: " + twoDay_res)
            # print("三天: " + threeDay_res)

            result = ''
            if oneDay_res or twoDay_res or threeDay_res:
                result = '可操作'
            else:
                result = '不可操作'
            df_tmp = pd.DataFrame([[id, self.__stockMap[id], oneDay_res, twoDay_res, threeDay_res, result]], columns=columns)
            df_result = df_result.append(df_tmp)
        return df_result


    ########################################################################################################################
    def oneDayAnalysisIndicators(self, df: DataFrame):
        if self.__analysis_days == -1:
            self.__analysis_days = len(df)
        resResult = ""
        for i in range(0, self.__analysis_days):
            line_lst = list(df.iloc[i])
            date, open, high, close, low = line_lst[0:5]
            day = [open, high, close, low]
            resResult += StockKLineFormChecker().checkSingleKLineForm(date, day)
        return resResult


    def twoDayAnalysisIndicators(self, df: DataFrame):
        if self.__analysis_days == -1:
            self.__analysis_days = len(df)-1
        resResult = ""
        for i in range(0, self.__analysis_days):
            dayOne = list(df.iloc[i + 1])
            dayTwo = list(df.iloc[i])
            date = dayOne[0]
            resResult += StockKLineFormChecker().checkDoubleKLineForm(date, dayOne, dayTwo)
        return resResult


    def threeDayAnalysisIndicators(self, df: DataFrame):
        if self.__analysis_days == -1:
            self.__analysis_days = len(df)-2
        resResult = ""
        for i in range(0, self.__analysis_days):
            dayOne = list(df.iloc[i + 2])
            dayTwo = list(df.iloc[i + 1])
            dayThree = list(df.iloc[i])
            date = dayTwo[0]
            print('---------------------------: ' + dayOne[0] + "|" + dayTwo[0] + "|" + dayThree[0])
            resResult += StockKLineFormChecker().checkMultipleKLineForm(date, dayOne, dayTwo, dayThree)
        return resResult
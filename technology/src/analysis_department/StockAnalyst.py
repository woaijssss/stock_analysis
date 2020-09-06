import pandas as pd
import datetime
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
            cls.__instance.init()
        return cls.__instance

    # 初始化部分默认股票
    def init(self):
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

    def test(self):
        print('+++: ', self.__stockMap)

    def setCode2Name(self, code:str, name:str):
        self.__stockMap[code] = name

    def getNameByCode(self, code:str):
        return self.__stockMap[code]

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

    '''
        - 根据当前数据量大小，和配置设置的分析周期，计算实际需要分析的数据天数
    '''
    def setAnalysisDays(self, df: DataFrame):
        if self.__analysis_days == -1:
            self.__analysis_days = len(df)
        else:   # analysis_days配置不为 -1
            startDate = ConfigLoader().get("stocks", "history_data_start_date")
            if startDate == '-1':   # 只计算7天的量
                self.__analysis_days = 7 if len(df) >= 7 else len(df)
            else:
                # 计算数据起始日期距离现在的天数
                year, mon, day = startDate.split('-')
                d1 = datetime.datetime(int(year), int(mon), int(day))
                d2 = datetime.datetime.now()  # 第二个日期
                days = (d2-d1).days
                self.__analysis_days = len(df) if days>len(df) else days


    ########################################################################################################################
    def oneDayAnalysisIndicators(self, df: DataFrame):
        self.setAnalysisDays(df)

        resResult = ""
        for i in range(0, self.__analysis_days):
            line_lst = list(df.iloc[i])
            date, open, high, close, low = line_lst[0:5]
            day = [open, high, close, low]
            resResult += StockKLineFormChecker().checkSingleKLineForm(date, day)
        return resResult


    def twoDayAnalysisIndicators(self, df: DataFrame):
        self.setAnalysisDays(df)

        resResult = ""
        for i in range(0, self.__analysis_days-1):
            dayOne = list(df.iloc[i + 1])
            dayTwo = list(df.iloc[i])
            date = dayOne[0]
            resResult += StockKLineFormChecker().checkDoubleKLineForm(date, dayOne, dayTwo)
        return resResult


    def threeDayAnalysisIndicators(self, df: DataFrame):
        self.setAnalysisDays(df)

        resResult = ""
        for i in range(0, self.__analysis_days-2):
            dayOne = list(df.iloc[i + 2])
            dayTwo = list(df.iloc[i + 1])
            dayThree = list(df.iloc[i])
            date = dayTwo[0]
            resResult += StockKLineFormChecker().checkMultipleKLineForm(date, dayOne, dayTwo, dayThree)
        return resResult
import os
import pandas as pd
import datetime
from pandas import DataFrame
from src.stock_forms.StockKLineFormChecker import StockKLineFormChecker
from auxiliary_lib.ConfigLoader import ConfigLoader
from src.analysis_department.CurveDeterminer import CurveDeterminer
from src.analysis_department.StockForms import StockForms

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

    '''
        设置 股票代码——股票名称 对应关系
    '''
    def setCode2Name(self, code:str, name:str):
        self.__stockMap[code] = name

    '''
        根据 股票代码 获取股票名称
    '''
    def getNameByCode(self, code:str):
        return self.__stockMap[code]

    '''
        K线形态分析
    '''
    def startAnalysisKLineForm(self):
        columns = ["股票代码", "股票名称", "一天形态", "两天形态", "多天形态", "5日均线趋势", "操作决策"]
        df_result = DataFrame(columns=columns)
        for id in self.__stockMap.keys():
            # 趋势线形态
            curveShape = -1
            if not os.path.exists(self.__root_path + id + self.__stockMap[id] + '.xlsx'):
                continue
            df = pd.read_excel(self.__root_path + id + self.__stockMap[id] + '.xlsx', sheet_name='历史日K数据',
                               parse_dates=True)
            print('-----------------------------: ' + id + self.__stockMap[id])

            self.setAnalysisDays(df)
            if ConfigLoader().get("stocks", "use_ma5") == '1':
                # 倒序排列5日均价数据
                ma5_list = list(df['5日均价'])[0:self.__analysis_days][::-1]
                size = len(ma5_list)
                curveShape = CurveDeterminer().curveUnevennessJudgment(ma5_list)

            oneDay_res_list = self.oneDayAnalysisIndicators(df)
            twoDay_res_list = self.twoDayAnalysisIndicators(df)
            threeDay_res_list = self.threeDayAnalysisIndicators(df)

            oneDay_res = ""
            twoDay_res = ""
            threeDay_res = ""
            '''
            form_condition = twoDay_res or threeDay_res
            if curveShape == -1:
                if form_condition:
                    result = "无趋势线，注意操作"
                else:
                    result = "无趋势线，不可操作"
            elif curveShape == 0 and form_condition:
                result = "买入"
            elif curveShape == 1 and form_condition:
                result = "卖出"
            else:
                result = "观望"
            '''
            result = "观望"
            if curveShape == -1:
                    result = "无趋势线"
            elif curveShape == 0:
                # print(oneDay_res_list)
                # print(twoDay_res_list)
                # print(threeDay_res_list)
                for date, code_list in oneDay_res_list:
                    for code in code_list:
                        if code in StockForms().getButtomFlipForm():
                            oneDay_res += date + StockForms().get(code)
                            result = "买入"
                for date, code_list in twoDay_res_list:
                    for code in code_list:
                        if code in StockForms().getButtomFlipForm():
                            twoDay_res += date + StockForms().get(code)
                            result = "买入"
                for date, code_list in threeDay_res_list:
                    for code in code_list:
                        if code in StockForms().getButtomFlipForm():
                            threeDay_res += date + StockForms().get(code)
                            result = "买入"
            elif curveShape == 1:
                for date, code_list in oneDay_res_list:
                    for code in code_list:
                        if code in StockForms().getTopFlipForm():
                            oneDay_res += date + StockForms().get(code)
                            result = "卖出"
                for date, code_list in twoDay_res_list:
                    for code in code_list:
                        if code in StockForms().getTopFlipForm():
                            twoDay_res += date + StockForms().get(code)
                            result = "卖出"
                for date, code_list in threeDay_res_list:
                    for code in code_list:
                        if code in StockForms().getTopFlipForm():
                            threeDay_res += date + StockForms().get(code)
                            result = "卖出"


            list2Df = [[id, self.__stockMap[id], oneDay_res, twoDay_res, threeDay_res, CurveDeterminer().getChnByTrendCode(curveShape), result]]
            df_tmp = pd.DataFrame(list2Df, columns=columns)
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
    # 一日形态
    def oneDayAnalysisIndicators(self, df: DataFrame):
        self.setAnalysisDays(df)

        # resResult = ""
        resList = []
        for i in range(0, self.__analysis_days):
            line_lst = list(df.iloc[i])
            date, open, high, close, low = line_lst[0:5]
            day = [open, high, close, low]
            res_code_list = StockKLineFormChecker().checkSingleKLineForm(date, day)
            if not res_code_list:
                continue
            resList.append([date, res_code_list])
        return resList

    # 两日组合形态
    def twoDayAnalysisIndicators(self, df: DataFrame):
        # resResult = ""
        resList = []
        for i in range(0, self.__analysis_days-1):
            dayOne = list(df.iloc[i + 1])
            dayTwo = list(df.iloc[i])
            date = dayOne[0]
            res_code_list = StockKLineFormChecker().checkDoubleKLineForm(date, dayOne, dayTwo)
            if not res_code_list:
                continue
            resList.append([date, res_code_list])
        return resList

    # 多日组合形态
    def threeDayAnalysisIndicators(self, df: DataFrame):
        # resResult = ""
        resList = []
        for i in range(0, self.__analysis_days-2):
            dayOne = list(df.iloc[i + 2])
            dayTwo = list(df.iloc[i + 1])
            dayThree = list(df.iloc[i])
            date = dayTwo[0]
            res_code_list = StockKLineFormChecker().checkMultipleKLineForm(date, dayOne, dayTwo, dayThree)
            if not res_code_list:
                continue
            resList.append([date, res_code_list])
        return resList
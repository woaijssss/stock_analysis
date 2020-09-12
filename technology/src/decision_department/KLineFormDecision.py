from pandas import DataFrame
from src.analysis_department.StockForms import StockForms
from src.stock_forms.StockKLineFormChecker import StockKLineFormChecker

"""
    K线形态决策
"""


class KLineFormDecision(object):
    __instance = None
    __kline_form_decision = {}

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance.init()
        return cls.__instance

    def init(self):
        self.__kline_form_decision[0] = "买入"
        self.__kline_form_decision[1] = "卖出"
        self.__kline_form_decision[2] = "观望"

    def getKLineDecisionResult(self, code: int):
        if code is None or code not in self.__kline_form_decision.keys():
            return '异常[K线形态]'
        return self.__kline_form_decision[code]

    def decision(self, curveShape:int, analysis_days: int, df: DataFrame):
        oneDay_res_list = self.oneDayAnalysisIndicators(analysis_days, df)
        twoDay_res_list = self.twoDayAnalysisIndicators(analysis_days, df)
        threeDay_res_list = self.threeDayAnalysisIndicators(analysis_days, df)
        return self.detail(curveShape, oneDay_res_list, twoDay_res_list, threeDay_res_list)

    def detail(self, curveShape:int, oneDay_res_list:list, twoDay_res_list:list, threeDay_res_list:list):
        oneDay_res = ""
        twoDay_res = ""
        threeDay_res = ""
        """
            按照分析天数返回决策结果：
                0：买入
                1：卖出
                2：观望
        """
        result_day1, result_day2, result_day3 = 2, 2, 2

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
            for date, code_list in oneDay_res_list:
                for code in code_list:
                    if code in StockForms().getButtomFlipForm():
                        oneDay_res += date + StockForms().get(code)
                        result_day1 = 0
            for date, code_list in twoDay_res_list:
                for code in code_list:
                    if code in StockForms().getButtomFlipForm():
                        twoDay_res += date + StockForms().get(code)
                        result_day2 = 0
            for date, code_list in threeDay_res_list:
                for code in code_list:
                    if code in StockForms().getButtomFlipForm():
                        threeDay_res += date + StockForms().get(code)
                        result_day3 = 0
        elif curveShape == 1:
            for date, code_list in oneDay_res_list:
                for code in code_list:
                    if code in StockForms().getTopFlipForm():
                        oneDay_res += date + StockForms().get(code)
                        result_day1 = 1
            for date, code_list in twoDay_res_list:
                for code in code_list:
                    if code in StockForms().getTopFlipForm():
                        twoDay_res += date + StockForms().get(code)
                        result_day2 = 1
            for date, code_list in threeDay_res_list:
                for code in code_list:
                    if code in StockForms().getTopFlipForm():
                        threeDay_res += date + StockForms().get(code)
                        result_day3 = 1
        return result_day1, result_day2, result_day3, oneDay_res, twoDay_res, threeDay_res

    ########################################################################################################################
    # 一日形态
    def oneDayAnalysisIndicators(self, analysis_days: int, df: DataFrame):
        # self.setAnalysisDays(df)
        # resResult = ""
        resList = []
        for i in range(0, analysis_days):
            line_lst = list(df.iloc[i])
            date, open, high, close, low = line_lst[0:5]
            day = [open, high, close, low]
            res_code_list = StockKLineFormChecker().checkSingleKLineForm(date, day)
            if not res_code_list:
                continue
            resList.append([date, res_code_list])
        return resList

    # 两日组合形态
    def twoDayAnalysisIndicators(self, analysis_days: int, df: DataFrame):
        # resResult = ""
        resList = []
        for i in range(0, analysis_days - 1):
            dayOne = list(df.iloc[i + 1])
            dayTwo = list(df.iloc[i])
            date = dayOne[0]
            res_code_list = StockKLineFormChecker().checkDoubleKLineForm(date, dayOne, dayTwo)
            if not res_code_list:
                continue
            resList.append([date, res_code_list])
        return resList

    # 多日组合形态
    def threeDayAnalysisIndicators(self, analysis_days: int, df: DataFrame):
        # resResult = ""
        resList = []
        for i in range(0, analysis_days - 2):
            dayOne = list(df.iloc[i + 2])
            dayTwo = list(df.iloc[i + 1])
            dayThree = list(df.iloc[i])
            date = dayTwo[0]
            res_code_list = StockKLineFormChecker().checkMultipleKLineForm(date, dayOne, dayTwo, dayThree)
            if not res_code_list:
                continue
            resList.append([date, res_code_list])
        return resList

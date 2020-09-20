import numpy as np
from pandas import DataFrame

"""
    换手率计算器
"""

class Turnover(object):
    __instance = None
    __turnover_code2Name = {}

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance.init()
        return cls.__instance

    def init(self):
        self.__turnover_code2Name[-1] = "停牌或异常"
        self.__turnover_code2Name[0] = "减少"
        self.__turnover_code2Name[1] = "增加"
        self.__turnover_code2Name[2] = "巨减"
        self.__turnover_code2Name[3] = "巨增"
        self.__turnover_code2Name[4] = "恒定"

    def getChnByKeyCode(self, code: int):
        if code is None or code not in self.__turnover_code2Name.keys():
            return '异常[换手率]'
        return self.__turnover_code2Name[code]

    def calcTurnover(self, analysis_days: int, df: DataFrame):
        end = 7 if len(df) >= 7 and analysis_days < 7 else analysis_days
        dataList = list(df['换手率（%）'])[0:end][::-1]

        length = len(dataList)
        if not length or length == 1:  # 散点为空或者长度为1，不符合判定标准
            return -1

        end_day_turnover = list(df['换手率（%）'])[length-1]
        mean_value = np.mean(dataList)
        if end_day_turnover < mean_value:
            return 0
        elif end_day_turnover > mean_value:
            return 1
        elif end_day_turnover*5 < mean_value:
            return 2
        elif end_day_turnover > mean_value*5:
            return 3
        else:
            return 4

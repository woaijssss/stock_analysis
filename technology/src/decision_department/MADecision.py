from pandas import DataFrame
from src.analysis_department.CurveDeterminer import CurveDeterminer

"""
    均线决策
"""


class MADecision(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def decision(self, analysis_days: int, df: DataFrame):
        # 倒序排列5日均价数据
        end = 7 if len(df) >= 7 and analysis_days < 7 else analysis_days
        ma5_list = list(df['5日均价'])[0:end][::-1]
        close_list = list(df['收盘价'])[0:end][::-1]
        size = len(ma5_list)
        # TODO
        '''
            对于短时趋势，5日均线存在延后的问题，因此暂时使用每日收盘价作为判断依据
        '''
        # return CurveDeterminer().curveUnevennessJudgment(ma5_list)
        return CurveDeterminer().curveUnevennessJudgment(close_list)
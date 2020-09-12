from pandas import DataFrame
from src.analysis_department.CurveDeterminer import CurveDeterminer

"""
    成交量决策
"""


class VolumeDecision(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def decision(self, analysis_days: int, df: DataFrame):
        # 倒序排列成交量数据
        end = 7 if len(df) >= 7 else analysis_days
        end = analysis_days + 1 if analysis_days == 1 else analysis_days
        volume_list = list(df['成交量（手）'])[0:end][::-1]
        size = len(volume_list)
        return CurveDeterminer().volumeSituation(volume_list)

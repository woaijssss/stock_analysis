import os
import pandas as pd
import datetime
from pandas import DataFrame
from src.stock_forms.StockKLineFormChecker import StockKLineFormChecker
from auxiliary_lib.ConfigLoader import ConfigLoader
from src.analysis_department.CurveDeterminer import CurveDeterminer
from src.analysis_department.StockForms import StockForms
from src.decision_department.MADecision import MADecision
from src.decision_department.VolumeDecision import VolumeDecision
from src.decision_department.KLineFormDecision import KLineFormDecision
from src.analysis_department.Turnover import Turnover

'''
    股票数据分析器
'''


class StockAnalyst(object):
    __root_path = "../datas/股票数据/"
    __stockMap = {}
    __instance = None
    __analysis_days = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance.init()
        return cls.__instance

    # 初始化部分默认股票
    def init(self):
        # self.__stockMap = {
        #     "000524": "岭南控股",
        #     "002108": "沧州明珠",
        #     "002138": "顺络电子",
        #     "002407": "多氟多",
        #     "002625": "光启技术",
        #     "600776": "东方通信",
        #     "603703": "盛洋科技",
        #     "603869": "新智认知",
        #     "600988": "赤峰黄金"
        # }
        pass

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
        columns = [
            "股票代码",
            "股票名称",
            "一天形态",
            "一天决策",
            "两天形态",
            "两天决策",
            "多天形态",
            "多天决策",
            "5日均线趋势",
            "量能情况",
            "换手率情况",
            "最终决策"
        ]
        df_result = DataFrame(columns=columns)
        df_purchased = DataFrame(columns=columns)
        df_monitor = DataFrame(columns=columns)
        code_list = ConfigLoader().get("stocks", "code_list").split(",")
        monitor_code_list = ConfigLoader().get("stocks", "monitor_code_list").split(",")

        count = 0
        stockCount = len(self.__stockMap)
        for id in self.__stockMap.keys():
            # 趋势线形态
            curveShape = -1
            count += 1

            # 读取股票数据文件
            if not os.path.exists(self.__root_path + id + self.__stockMap[id] + '.xlsx'):
                continue
            df = pd.read_excel(self.__root_path + id + self.__stockMap[id] + '.xlsx', sheet_name='历史日K数据', parse_dates=True)

            # 计算分析天数
            self.setAnalysisDays(df)
            print('第 %d 只/共%d只: [%s], 分析天数起始值: [%d]' % (count, stockCount, id + self.__stockMap[id], self.__analysis_days))

            # 判定5日均线趋势
            if ConfigLoader().get("stocks", "use_ma5") == '1':
                curveShape = MADecision().decision(self.__analysis_days, df)

            # 判定成交量情况
            volume_situation = VolumeDecision().decision(self.__analysis_days, df)

            # 判定换手率情况
            turnover_situation = Turnover().calcTurnover(self.__analysis_days, df)

            # 判定K线形态
            result_day1, result_day2, result_day3, oneDay_res, twoDay_res, threeDay_res = KLineFormDecision().decision(curveShape, self.__analysis_days, df)

            # 判定最终决策
            '''
                - 两个以上指标决策为买入，最终才能买入
                - 一个以上指标决策为卖出，最终结果卖出
                - 其他情况全部观望
            '''
            result_list = [result_day1, result_day2, result_day3]
            final_result = 2
            if result_list.count(0) >= 1 and result_list.count(1) == 0:   # 买入决策
                final_result = 0
            elif result_list.count(1) >= 1 and result_list.count(0) == 0: # 卖出决策
                final_result = 1

            list2Df = [[
                id,
                self.__stockMap[id],
                oneDay_res, KLineFormDecision().getKLineDecisionResult(result_day1),
                twoDay_res, KLineFormDecision().getKLineDecisionResult(result_day2),
                threeDay_res, KLineFormDecision().getKLineDecisionResult(result_day3),
                CurveDeterminer().getChnByTrendCode(curveShape),
                CurveDeterminer().gtChnByVolumeSituation(volume_situation),
                Turnover().getChnByKeyCode(turnover_situation),
                KLineFormDecision().getKLineDecisionResult(final_result)
            ]]

            df_tmp = pd.DataFrame(list2Df, columns=columns)
            df_result = df_result.append(df_tmp)

            ## 单独保存已经购买的股票
            if id in code_list:
                df_purchased = df_purchased.append(df_tmp)

            ## 保存加入监控的股票
            if id in monitor_code_list:
                df_monitor = df_monitor.append(df_tmp)

        return df_result, df_purchased, df_monitor

    '''
        - 根据当前数据量大小，和配置设置的分析周期，计算实际需要分析的数据天数
    '''
    def setAnalysisDays(self, df: DataFrame):
        self.__analysis_days = int(ConfigLoader().get("stocks", "analysis_days"))
        if self.__analysis_days == -1:  # 仅供测试
            self.__analysis_days = len(df)
        else:   # analysis_days配置不为 -1
            analysis_days_temp = 0
            startDate = ConfigLoader().get("stocks", "history_data_start_date")
            if startDate == '-1':   # 只计算7天的量
                analysis_days_temp = 7 if len(df) >= 7 else len(df)
            else:
                # 计算数据起始日期距离现在的天数
                year, mon, day = startDate.split('-')
                d1 = datetime.datetime(int(year), int(mon), int(day))
                d2 = datetime.datetime.now()  # 第二个日期
                days = (d2-d1).days
                analysis_days_temp = len(df) if days>len(df) else days
            self.__analysis_days = min(self.__analysis_days, analysis_days_temp)



from pandas import DataFrame
from src.stock_forms.SingleKLineFormChecker import SingleKLineFormChecker
from src.stock_forms.DoubleKLineFormChecker import DoubleKLineFormChecker
from src.stock_forms.MultipleKLineFormChecker import MultipleKLineFormChecker

'''
    - 单例模式
    - 股票形态检测器
    - 股票形态检测标准：
    （1） 反转形态：
        - 检测近期的均线趋势（判断上涨或下跌行情）
        - 检测当日或（最多近3日）的K线组合形态是否存在反转形态
    （2） 持续形态：
        - 检测近期的均线趋势（判断上涨或下跌行情）
        - 检测当日或（最近3日）的K线组合形态是否存在持续形态
    （3） 十字星形态：
        - 当日是否以十字星收盘
        - 如果是以十字星收盘，则判断是否存在跳空、启明星、黄昏星等强烈反转信号
    （4） 判别形态主要以价格参数为依据，因此可分为：
        - 单日价格形态判别（只需要当前交易日的价格数据即可）
        - 两日价格形态判别（需要当前交易日和上一个交易日的价格数据）
        - 三日价格形态判别（需要当前交易日和上两个交易日的价格数据）
'''
class StockKLineFormChecker(object):
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    '''
        单K线形态检测
    '''
    def checkSingleKLineForm(self, day:list):
        return SingleKLineFormChecker().hammerWire(day)

    '''
        双K线形态检测
    '''
    def checkDoubleKLineForm(self, dayOne:list, dayTwo:list):
        # TODO 增加同时检测多种形态
        return (DoubleKLineFormChecker().engulfingForm(dayOne, dayTwo)
                or DoubleKLineFormChecker().darkCloudCover(dayOne, dayTwo)
                or DoubleKLineFormChecker().piercingForm(dayOne, dayTwo))

    '''
        多K线形态检测
    '''
    def checkMultipleKLineForm(self, dayOne:list, dayTwo:list, dayThree:list):
        return (MultipleKLineFormChecker().venusForm(dayOne, dayTwo, dayThree)
                or MultipleKLineFormChecker().eveningStarForm(dayOne, dayTwo, dayThree)
                or MultipleKLineFormChecker().crossVenusForm(dayOne, dayTwo, dayThree)
                or MultipleKLineFormChecker().crossEveningStarForm(dayOne, dayTwo, dayThree))



########################################################################################################################
def testOneDay(df:DataFrame):
    resList = []
    for i in range(0, len(df)):
            line_lst = list(df.iloc[i])
            date, open, high, close, low = line_lst[0:5]
            day = [open, high, close, low]
            if StockKLineFormChecker().checkSingleKLineForm(day):
                resList.append(date)
    print("一天的指标： ", resList)

def testTwoDay(df:DataFrame):
    resList = []
    for i in range(0, len(df) - 1):
        dayOne = list(df.iloc[i + 1])
        dayTwo = list(df.iloc[i])
        if StockKLineFormChecker().checkDoubleKLineForm(dayOne, dayTwo):
            resList.append(dayOne[0])
    print("两天的指标： ", resList)

def testThreeDay(df: DataFrame):
    resList = []
    for i in range(0, len(df) - 2):
        dayOne = list(df.iloc[i + 2])
        dayTwo = list(df.iloc[i + 1])
        dayThree = list(df.iloc[i])
        if StockKLineFormChecker().checkMultipleKLineForm(dayOne, dayTwo, dayThree):
            resList.append(dayTwo[0])
    print("三天的指标： ", resList)

if __name__ == '__main__':
    import pandas as pd
    stockMap = {
        "000524": "岭南控股",
        "002108": "沧州明珠",
        "002138": "顺络电子",
        "002407": "多氟多",
        "002625": "光启技术",
        "600776": "东方通信",
        "603703": "盛洋科技",
        "603869": "新智认知"
    }

    for id in stockMap.keys():
        df = pd.read_excel('../../datas/股票数据/' + id + stockMap[id] + '.xlsx', sheet_name='历史日K数据', parse_dates=True)
        print('-----------------------------: ' + id + stockMap[id])
        testOneDay(df)
        testTwoDay(df)
        testThreeDay(df)
        print('===========================================\n')
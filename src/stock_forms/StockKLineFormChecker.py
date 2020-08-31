
from pandas import DataFrame

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

    # 锤子线
    def hammerWire(self, df:DataFrame):
        resList = []
        for i in range(0, len(df)):
            line_lst = list(df.iloc[i])
            open, high, close, low = line_lst[1:5]
            entity_len = abs(open-close)    # K线实体
            upper_shadow_len = high-open if open > close else high-close
            # 长下影线 and 无上影线或极短的下影线
            if (abs(low-open) > 2*entity_len or abs(low-close) > 2*entity_len) \
                    and upper_shadow_len < 0.05:
                resList.append(line_lst[0])
        return resList

    # 吞没形态
    def engulfingForm(self, df:DataFrame):
        resList = []
        for i in range(0, len(df)-1):
            lst1 = list(df.iloc[i+1])
            lst2 = list(df.iloc[i])
            open1, high1, close1, low1 = lst1[1:5]
            open2, high2, close2, low2 = lst2[1:5]
            # 看跌 or 看涨
            if (open1<close1 and open2>close2 and open2>close1) or (open1>close1 and open2<close2 and close2>open1):
                if abs(open1-close1) < abs(open2-close2):
                    resList.append(lst1[0])
        return resList

if __name__ == '__main__':
    import pandas as pd
    df = pd.read_excel('../../datas/股票数据/603703盛洋科技.xlsx', sheet_name='历史日K数据', parse_dates=True)
    # resList = StockKLineFormChecker().hammerWire(df)
    resList = StockKLineFormChecker().engulfingForm(df)
    print(resList)
"""
    两根K线构成的形态的检测器
"""
'''
    # 吞没形态
    # 乌云盖顶形态
    # 刺透形态（斩回线形态）
    # 倒锤子形态
    # 孕线形态              # -------孕线形态与十字孕线在顶部反转信号更强烈
    # 十字孕线形态
    # 平头顶部
    # 平头底部
'''


class DoubleKLineFormChecker(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    # 吞没形态
    def engulfingForm(self, dayOne: list, dayTwo: list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        # 第二根K线完全包裹住第一根K线
        # 看跌条件
        condition1 = (open2 > close1 > open1 > close2 and open2 > close2)
        condition2 = (close2 > open1 > close1 > open2 and open2 < close2)
        '''
            - 第二根K线完全包裹住第一根K线
        '''
        if (condition1 or condition2) and abs(open1 - close1) < abs(open2 - close2):
            return 0x100
        return -1

    # 乌云盖顶形态
    def darkCloudCover(self, dayOne: list, dayTwo: list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        '''
            - 第二日开盘价高于第一日最高价
            - 第二日的阴线深入到阳线 1/2 以下（深入越多越好）
        '''
        if high1 < open2 \
                and open1 < close2 < (open1 + close1) / 2:
            return 0x101
        return -1

    # 刺透形态（斩回线形态）
    def piercingForm(self, dayOne: list, dayTwo: list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        '''
            - 第二天的阳线必须向上刺透第一天阴线 1/2 以上（刺透越多越好）
        '''
        if open1 > close1 and open2 < close2 and \
                (low1 >= open2 or close1 >= open2) and close2 < open1 and close2 > (open1 + close1) / 2:
            return 0x102
        return -1

    # 倒锤子形态
    def invertedHammerWire(self, dayOne: list, dayTwo: list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        entity_len = abs(open1 - close1)  # K线实体
        lower_shadow_len = open1 - low1 if open1 < close1 else close1 - low1
        max1 = max(open1, close1)
        '''
            - 实体较小
            - 长上影线
            - 颜色不重要
            - 第二天是一根阳线，并且阳线 开盘价 >= 第一天实体的最大值
        '''
        if abs(high1 - max1) > 2 * entity_len \
                and lower_shadow_len < 0.01 \
                and close2 > open2 >= max1:
            return 0x103
        return -1

    # 孕线形态
    def pregnantLineForm(self, dayOne: list, dayTwo: list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        entity_len1, entity_len2 = abs(open1 - close1), abs(open2 - close2)
        min1, max1 = min(open1, close1), max(open1, close1)
        min2, max2 = min(open2, close2), max(open2, close2)

        '''
            - 第二根K线颜色不重要
        '''
        if min1 <= min2 and max1 >= max2 and entity_len1 >= 3*entity_len2:
            if open1 < close1:
                return 0x104
            elif open1 > close1:
                return 0x105
        return -1

    # 十字孕线形态
    def crossPregnantLineForm(self, dayOne: list, dayTwo: list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        entity_len1, entity_len2 = abs(open1 - close1), abs(open2 - close2)
        min1, max1 = min(open1, close1), max(open1, close1)
        min2, max2 = min(open2, close2), max(open2, close2)

        '''
            - 第二根K线颜色不重要
        '''
        if min1 < min2 and max1 > max2 and entity_len1 >= 3*entity_len2 and entity_len2 <= 0.005:
            if open1 < close1:
                return 0x106
            elif open1 > close1:
                return 0x107
        return -1

    # 平头顶部
    def flatTopForm(self, dayOne: list, dayTwo: list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        upper_shadow_len1 = high1 - open1
        upper_shadow_len2 = high2 - open2

        '''
            - 实体一样高或上影线一样高
            - 可以相近，也可以相邻（这里计算相近的）
            - 第二根阴线实体在第一根实体内部才有意义
        '''
        ## 实体一样高
        condition1 = upper_shadow_len1 <= 0.005 and upper_shadow_len2 <= 0.005 and abs(close1 - open2) <= 0.005
        ## 上影线一样高
        condition2 = upper_shadow_len1 > 0.005 and upper_shadow_len2 > 0.005 and abs(high1 - high2) <= 0.005
        if open1 < close1 and open2 > close2 \
                and (open1 < close2 < close1 or open1 < open2 < close1) \
                and (condition1 or condition2):
            return 0x108
        return -1

    # 平头底部
    def flatBottomForm(self, dayOne: list, dayTwo: list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        lower_shadow_len1 = open1 - low1 if open1 < close1 else close1 - low1
        lower_shadow_len2 = open2 - low2 if open2 < close2 else close2 - low2

        '''
            - 实体一样高或上影线一样高
            - 可以相近，也可以相邻（这里计算相近的）
            - 第二根阴线实体在第一根实体内部才有意义
        '''
        ## 实体一样高
        condition1 = lower_shadow_len1 <= 0.005 and lower_shadow_len2 <= 0.005 and abs(close1 - open2) <= 0.005
        ## 下影线一样高
        condition2 = lower_shadow_len1 > 0.005 and lower_shadow_len2 > 0.005 and abs(low1 - low2) <= 0.005
        if open1 > close1 and open2 < close2 \
                and (open1 > close2 > close1 or open1 > open2 > close1) \
                and (condition1 or condition2):
            return 0x109
        return -1


if __name__ == '__main__':
    import pandas as pd
    stockMap = {
        "000524": "岭南控股",
        "002108": "沧州明珠",
        "002138": "顺络电子",
        "002625": "光启技术",
        "603703": "盛洋科技",
        "600988": "赤峰黄金",
        "000503": "国新健康",
        "300316": "晶盛机电",
        "300376": "易事特",
        "300424": "航新科技",
        "300494": "盛天网络"
    }

    import os
    from src.analysis_department.StockForms import StockForms

    for id in stockMap.keys():

        if not os.path.exists('../../datas/股票数据/' + id + stockMap[id] + '.xlsx'):
            continue

        df = pd.read_excel('../../datas/股票数据/' + id + stockMap[id] + '.xlsx', sheet_name='历史日K数据', parse_dates=True)
        print('-----------------------------: ' + id + stockMap[id])

        for i in range(0, 150):
            dayOne = list(df.iloc[i + 1])
            dayTwo = list(df.iloc[i])
            date = dayOne[0]
            res = DoubleKLineFormChecker().flatBottomForm(dayOne, dayTwo)
            if res != -1:
                print("====>: " + date + ": " + StockForms().get(res), end="")
        print('===========================================\n')

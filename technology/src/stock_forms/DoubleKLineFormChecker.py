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
    def InvertedHammerWire(self, dayOne: list, dayTwo: list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        entity_len = abs(open1 - close1)  # K线实体
        lower_shadow_len = open1 - low1 if open1 < close1 else close1 - low1
        max1 = max(open1, close1)
        '''
            - 实体较小
            - 长上影线
            - 颜色不重要
        '''
        if abs(high1 - max1) > 2 * entity_len \
                and lower_shadow_len < 0.05 \
                and close2 > open2 > max1:
            return 0x103
        return -1

    # 孕线形态
    def pregnantLineForm(self, dayOne: list, dayTwo: list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        entity_len1, entity_len2 = abs(open1 - close1), abs(open2 - close2)
        max2 = max(open2, close2)
        min2 = min(open2, close2)

        '''
            - 第二根K线颜色不重要
        '''
        if open1 < close1 and close1 > max2 and open1 < min2 \
                and entity_len1 >= 2 * entity_len2:
            return 0x104
        return -1

    # 十字孕线形态
    def crossPregnantLineForm(self, dayOne: list, dayTwo: list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        entity_len1, entity_len2 = abs(open1 - close1), abs(open2 - close2)
        max2 = max(open2, close2)
        min2 = min(open2, close2)

        '''
            - 第二根K线颜色不重要
        '''
        if open1 < close1 and close1 > max2 and open1 < min2 \
                and abs(open2 - close2) / open2 < 0.005 \
                and entity_len1 >= 2 * entity_len2:
            return 0x105
        return -1

    # 平头顶部
    def flatTopForm(self, dayOne: list, dayTwo: list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        upper_shadow_len1 = high1 - open1
        upper_shadow_len2 = high2 - open2

        condition1 = abs(high1 - high2) / high1 < 0.001
        condition2 = upper_shadow_len1 < 0.001 and upper_shadow_len2 < 0.001 and abs(close1 - open2) / close1 < 0.001
        if open1 < close1 and open2 > close2 and (condition1 or condition2):
            return 0x106
        return -1

    # 平头底部
    def flatBottomForm(self, dayOne: list, dayTwo: list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        lower_shadow_len1 = open1 - low1 if open1 < close1 else close1 - low1
        lower_shadow_len2 = open2 - low2 if open2 < close2 else close2 - low2

        condition1 = abs(low1 - low2) / low1 < 0.001
        condition2 = lower_shadow_len1 < 0.01 and lower_shadow_len2 < 0.01 and abs(close1 - open2) / close1 < 0.01
        if open1 > close1 and open2 < close2 and (condition1 or condition2):
            return 0x107
        return -1


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
        "603869": "新智认知",
        "600988": "赤峰黄金",
        '002416': '爱施德'
    }

    for id in stockMap.keys():
        import os

        if not os.path.exists('../../datas/股票数据/' + id + stockMap[id] + '.xlsx'):
            continue

        df = pd.read_excel('../../datas/股票数据/' + id + stockMap[id] + '.xlsx', sheet_name='历史日K数据', parse_dates=True)
        print('-----------------------------: ' + id + stockMap[id])

        for i in range(0, 150):
            dayOne = list(df.iloc[i + 1])
            dayTwo = list(df.iloc[i])
            date = dayOne[0]
            if DoubleKLineFormChecker().flatTopForm(dayOne, dayTwo) != -1:
                print("====: " + date)
        print('===========================================\n')

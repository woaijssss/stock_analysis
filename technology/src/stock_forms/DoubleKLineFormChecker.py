
'''
    两根K线构成的形态的检测器
'''
'''
    # 吞没形态
    # 乌云盖顶形态
    # 刺透形态（斩回线形态）
'''
class DoubleKLineFormChecker(object):
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    # 吞没形态
    def engulfingForm(self, dayOne:list, dayTwo:list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        # 第二根K线完全包裹住第一根K线
        if (open1 < close1 and open2 > close2 and open2 > close1) \
                or (open1 > close1 and open2 < close2 and close2 > open1):
            if abs(open1 - close1) < abs(open2 - close2):
                return True
        return False

    # 乌云盖顶形态
    def darkCloudCover(self, dayOne:list, dayTwo:list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        '''
            - 第二日开盘价高于第一日最高价
            - 第二日的阴线深入到阳线 1/2 以下（深入越多越好）
        '''
        if high1 < open2  \
            and close2 > open1 and close2 < (open1+close1)/2:
            return True
        return False

    # 刺透形态（斩回线形态）
    def piercingForm(self, dayOne:list, dayTwo:list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        '''
            - 第二天的阳线必须向上刺透第一天阴线 1/2 以上（刺透越多越好）
        '''
        if open2 < low1 and close2 < open1 and close2 > (open1+close1)/2:
            return True
        return False

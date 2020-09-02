
'''
    多根K线构成的形态的检测器
'''
'''
    # 启明星形态
    # 黄昏星形态
    # 十字启明星
    # 十字黄昏星
'''
class MultipleKLineFormChecker(object):
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    # 启明星形态
    def venusForm(self, dayOne:list, dayTwo:list, dayThreee:list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        open3, high3, close3, low3 = dayThreee[1:5]

        '''
            - 第一天长阴线（未加“长”）
            - 第二天的为小实体（未判断“小”）
            - 第三天长阳线明显推入第一天的阴线实体中
        '''
        ## 条件一：两边都有跳空
        condition1 = open1 > close1 and open2 < close2 and open3 < close3 \
                     and close2 < close1 and close2 < open3 \
                     and open1 >= close3 and close1 < open3

        ## 条件二：只有一边有跳空
        condition2 = open1 > close1 and open2 < close2 and open3 < close3 \
                     and open2 < close1 and open2 < open3 and close2 < open1 and close2 < close3 \
                     and open1 >= close3 and (close3 > close1 and close3 < open1)
        if condition1 or condition2:
            return True
        return False

    # 黄昏星形态
    def eveningStarForm(self, dayOne:list, dayTwo:list, dayThreee:list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        open3, high3, close3, low3 = dayThreee[1:5]

        '''
            - 第一天长阳线（未加“长”）
            - 第二天的为小实体（未判断“小”）    
            - 第三天长阴线明显穿入第一天的阴线实体中    
        '''
        condition1 = open1 < close1 and open2 > close2 and open3 > close3 \
                     and open2 > close1 and open2 > open3 and close2 > open1 and close2 > close3 \
                    and (open3 > open1 and open3 < close1) \
                    and abs(open3-close3) > abs(open2-close2)
        if condition1:
            return True
        return False

    # 十字启明星形态
    def crossVenusForm(self, dayOne:list, dayTwo:list, dayThree:list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        open3, high3, close3, low3 = dayThree[1:5]

        '''
            - 第二天出现十字星线
        '''
        # 看涨
        condition1 = open1 > close1 and open2 < close2 and open3 < close3 \
                     and close2 < close1 and close2 < open3 \
                     and open1 >= close3 and close1 < open3


        condition2 = open1 > close1 and open2 < close2 and open3 < close3 \
                     and open2 < close1 and open2 < open3 and close2 < open1 and close2 < close3 \
                     and open1 >= close3 and (close3 > close1 and close3 < open1)
        if (condition1 or condition2) and abs(open2-close2)/open2 < 0.01:   # TODO 0.01精度需要测试调整
            return True
        return False

    # 十字黄昏星
    def crossEveningStarForm(self, dayOne:list, dayTwo:list, dayThreee:list):
        open1, high1, close1, low1 = dayOne[1:5]
        open2, high2, close2, low2 = dayTwo[1:5]
        open3, high3, close3, low3 = dayThreee[1:5]

        '''
            - 第二天出现十字星线
        '''
        # 看跌
        condition1 = open1 < close1 and open2 > close2 and open3 > close3 \
                     and open2 > close1 and open2 > open3 and close2 > open1 and close2 > close3 \
                    and (open3 > open1 and open3 < close1) \
                    and abs(open3-close3) > abs(open2-close2)
        if condition1 and abs(open2-close2)/open2 < 0.01:
            return True
        return False


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
        "600988": "赤峰黄金"
    }

    for id in stockMap.keys():
        df = pd.read_excel('../../datas/股票数据/' + id + stockMap[id] + '.xlsx', sheet_name='历史日K数据', parse_dates=True)
        print('-----------------------------: ' + id + stockMap[id])

        for i in range(0, len(df) - 2):
            dayOne = list(df.iloc[i + 2])
            dayTwo = list(df.iloc[i + 1])
            dayThree = list(df.iloc[i])
            date = dayTwo[0]
            if MultipleKLineFormChecker().crossVenusForm(dayOne, dayTwo, dayThree):
                print("一天: " + date)
        print('===========================================\n')
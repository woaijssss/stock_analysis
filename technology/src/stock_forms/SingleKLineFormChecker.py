
'''
    单根K线构成的形态的检测器
'''
'''
    # 锤子线
    # 十字星线
'''
class SingleKLineFormChecker(object):
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    # 锤子线
    def hammerWire(self, day:list):
        open, high, close, low = day[0:4]
        entity_len = abs(open - close)  # K线实体
        upper_shadow_len = high - open if open > close else high - close
        '''
            - 长下影线
            - 无上影线或极短的下影线
        '''
        if (abs(low - open) > 2 * entity_len or abs(low - close) > 2 * entity_len) \
                and upper_shadow_len < 0.01:
            return True
        return False

    # 流星形态
    ## 流星形态的高位看跌比低位看涨要强烈！！！
    def meteorForm(self, day:list):
        open, high, close, low = day[0:4]
        entity_len = abs(open - close)  # K线实体
        lower_shadow_len = open - low if open < close else close - low
        '''
            - 实体较小
            - 长上影线
            - 颜色不重要
        '''
        if (abs(high - open) > 2 * entity_len or abs(high - close) > 2 * entity_len) \
                and lower_shadow_len < 0.01:
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

        for i in range(0, len(df)):
            line_lst = list(df.iloc[i])
            date, open, high, close, low = line_lst[0:5]
            day = [open, high, close, low]
            if SingleKLineFormChecker().meteorForm(day):
                print("====: " + date)
        print('===========================================\n')
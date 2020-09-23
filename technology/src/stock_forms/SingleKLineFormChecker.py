
'''
    单根K线构成的形态的检测器
'''
'''
    # 锤子线
    # 流星形态
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
        lower_shadow_len = open - low if open < close else close - low
        '''
            - 长下影线
            - 无上影线
        '''
        if lower_shadow_len > 2 * entity_len and upper_shadow_len == 0: # 严格没有上影线
            if open > close:
                return 0x000    # 顶部绿锤子线
            elif open < close:
                return 0x001    # 底部红锤子线
        return -1

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
                and lower_shadow_len == 0:  # 严格没有下影线
            return 0x002
        return -1

    # 倒锤子形态
    def invertedHammerWire(self, day: list):
        open, high, close, low = day[0:4]
        entity_len = abs(open - close)  # K线实体
        lower_shadow_len = open - low if open < close else close - low
        max_v = max(open, close)
        '''
            - 实体较小
            - 长上影线
            - 颜色不重要
            - 第二天是一根阳线，并且阳线 开盘价 >= 第一天实体的最大值
        '''
        if abs(high - max_v) >= entity_len \
                and lower_shadow_len == 0:  # 严格无下影线
            return 0x104
        return -1

if __name__ == '__main__':
    import pandas as pd
    from src.analysis_department.StockForms import StockForms

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

    for id in stockMap.keys():
        df = pd.read_excel('../../datas/股票数据/' + id + stockMap[id] + '.xlsx', sheet_name='历史日K数据', parse_dates=True)
        print('-----------------------------: ' + id + stockMap[id])

        for i in range(0, len(df)):
            line_lst = list(df.iloc[i])
            date, open, high, close, low = line_lst[0:5]
            day = [open, high, close, low]
            res = SingleKLineFormChecker().hammerWire(day)
            if res != -1:
                print("====>: " + date + ": " + StockForms().get(res), end="")
        print('===========================================\n')

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
                and upper_shadow_len < 0.05:
            return True
        return False

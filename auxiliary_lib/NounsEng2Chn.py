
'''
    英文-->中文转换器
'''
class NounsEng2Chn(object):
    __instance = None
    mDataColumnsMap = {}    # 记录数据中，英文和中文的对应关系

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.mDataColumnsMap["code"] = "代码"
        self.mDataColumnsMap["name"] = "名称"
        self.mDataColumnsMap["changepercent"] = "涨跌幅（%）"
        self.mDataColumnsMap["trade"] = "现价（元）"
        self.mDataColumnsMap["open"] = "开盘价（元）"
        self.mDataColumnsMap["close"] = "收盘价（元）"
        self.mDataColumnsMap["high"] = "最高价（元）"
        self.mDataColumnsMap["low"] = "最低价（元）"
        self.mDataColumnsMap["settlement"] = "昨日收盘价（元）"
        self.mDataColumnsMap["volume"] = "成交量（股）"
        self.mDataColumnsMap["turnoverratio"] = "换手率（%）"
        self.mDataColumnsMap["amount"] = "成交额"
        self.mDataColumnsMap["per"] = "市盈率"
        self.mDataColumnsMap["pb"] = "市净率"
        self.mDataColumnsMap["mktcap"] = "总市值（万）"
        self.mDataColumnsMap["nmc"] = "流通市值（万）"

        self.mDataColumnsMap["price_change"] = "价格变动"
        self.mDataColumnsMap["p_change"] = "涨跌幅（%）"
        self.mDataColumnsMap["ma5"] = "5日均价"
        self.mDataColumnsMap["ma10"] = "10日均价"
        self.mDataColumnsMap["ma20"] = "20日均价"
        self.mDataColumnsMap["v_ma5"] = "5日均量"
        self.mDataColumnsMap["v_ma10"] = "10日均量"
        self.mDataColumnsMap["v_ma20"] = "20日均量"
        self.mDataColumnsMap["turnover"] = "换手率（%）"

    '''
        限定返回值类型为字典
    '''
    def getDataMap(self) -> dict:
        return self.mDataColumnsMap

    '''
        限定入参类型为str，str，返回值类型为空
    '''
    def setData(self, key:str, val:str) -> None:
        self.mDataColumnsMap[key] = val


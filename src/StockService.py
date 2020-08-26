
import tushare as ts
from stock_analysis.src.StockIndexDatasManager import StockIndexDatasManager

'''
    主服务入口
'''
class StockService(object):
    mPro = None
    __instance = None
    mIndexDataGetter = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        pro = ts.pro_api(token='063c3e42ec30996bf395ddb0b7875918b2280544dee0c7e657b8136d')

    def startService(self):
        mIndexDataManager = StockIndexDatasManager()
        mIndexDataManager.setPro(self.mPro)
        mIndexDataManager.getAllIndexInfo()

import tushare as ts
from stock_analysis.src.StockIndexDatasManager import StockIndexDatasManager
from stock_analysis.src.StockDatasManager import StockDatasManager
from stock_analysis.src.analysis_department.StockAnalyst import StockAnalyst

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
        self.mPro = ts.pro_api(token='e5ccd9b1da858f2e127afef26431dd550ebd8d837f2394816722f0f9')

    '''
        开启主服务
    '''
    def startService(self):
        self.startDataCollection()
        self.startDataAnalysis()

    '''
        开始获取基础数据
    '''
    def startDataCollection(self):
        self.getStockIndexDatas()       # 获取指数数据
        self.getStockDatas()            # 获取股票数据

    '''
        获取指数基础日K数据
    '''
    def getStockIndexDatas(self):
        mIndexDataManager = StockIndexDatasManager()
        mIndexDataManager.setPro(self.mPro)
        mIndexDataManager.getAllIndexDaily()

    '''
        获取股票基础信息、日K数据
    '''
    def getStockDatas(self):
        mStockDatasManager = StockDatasManager()
        mStockDatasManager.setPro(self.mPro)
        mStockDatasManager.getAllStockInfoPro()         # 从中获取A股代码
        mStockDatasManager.getAllStockHistoryDatas()    # 获取所有A股的历史数据

    '''
        开始进行股票数据分析
            - 技术指标分析
            - ML预测
    '''
    def startDataAnalysis(self):
        pass

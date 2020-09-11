from pandas import DataFrame

'''
    英文-->中文转换器
'''


class NounsEng2Chn(object):
    __instance = None
    mStockCode2Chn = {}  # 股票代码--中文对照关系
    mDataAllIndexInfo = {}  # 所有交易指数的基本数据               英文--中文对照关系
    mDataSpecIndexInfo = {}  # 特定交易指数的基本数据              英文--中文对照关系
    mDataSpecIndexTradingDaily = {}  # 特定交易指数的日K数据       英文--中文对照关系

    mDataAllStockBasicInfo = {}  # 获取A股所有股票的基础信息       英文--中文对照关系
    mDataTradingDaysMap = {}  # 记录A股当前交易日数据              英文--中文对照关系
    mDataSpecStockHistory = {}  # 记录特定股票的历史性数据         英文--中文对照关系

    mDataCompanyBasicInfo = {}  # 记录上市公司的基本情况           英文--中文对照关系
    mDataStockCompany = {}      # 记录上市公司的基本情况（pro接口） 英文--中文对照关系


    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    '''
        列名英文转中文
    '''

    def converseEng2Chn(self, df: DataFrame, name_dic: dict):
        for name in list(df.columns):
            if name in name_dic:
                df.rename(columns={name: name_dic[name]}, inplace=True)  # 修改列名
        return df

    '''
        股票代码转中文名字
    '''

    def converseStockCode2Chn(self, df: DataFrame):
        for i in range(0, len(df)):
            _, _, code, name, _, _, _, _ = df.iloc[i]
            self.mStockCode2Chn[code] = name

    def __init__(self):
        # get_index（）所有交易指数基本信息列
        self.mDataAllIndexInfo["code"] = "指数代码"
        self.mDataAllIndexInfo["name"] = "指数名称"
        self.mDataAllIndexInfo["change"] = "涨跌幅"
        self.mDataAllIndexInfo["open"] = "开盘价"
        self.mDataAllIndexInfo["preclose"] = "昨日收盘价"
        self.mDataAllIndexInfo["close"] = "收盘价"
        self.mDataAllIndexInfo["high"] = "最高价"
        self.mDataAllIndexInfo["low"] = "最低价"
        self.mDataAllIndexInfo["volume"] = "成交量(手)"
        self.mDataAllIndexInfo["amount"] = "成交金额（亿元）"

        # index_basic()特定交易指数基本信息列
        self.mDataSpecIndexInfo["ts_code"] = "TS代码"
        self.mDataSpecIndexInfo["name"] = "简称"
        self.mDataSpecIndexInfo["fullname"] = "指数全称"
        self.mDataSpecIndexInfo["market"] = "市场"
        self.mDataSpecIndexInfo["publisher"] = "发布方"
        self.mDataSpecIndexInfo["index_type"] = "指数风格"
        self.mDataSpecIndexInfo["category"] = "指数类别"
        self.mDataSpecIndexInfo["base_date"] = "基期"
        self.mDataSpecIndexInfo["base_point"] = "基点"
        self.mDataSpecIndexInfo["list_date"] = "发布日期"
        self.mDataSpecIndexInfo["weight_rule"] = "加权方式"
        self.mDataSpecIndexInfo["desc"] = "描述"
        self.mDataSpecIndexInfo["exp_date"] = "终止日期"

        # index_daily()特定交易指数日K数据列
        self.mDataSpecIndexTradingDaily["ts_code"] = "TS指数代码"
        self.mDataSpecIndexTradingDaily["trade_date"] = "交易日"
        self.mDataSpecIndexTradingDaily["close"] = "收盘点位"
        self.mDataSpecIndexTradingDaily["open"] = "开盘点位"
        self.mDataSpecIndexTradingDaily["high"] = "最高点位"
        self.mDataSpecIndexTradingDaily["low"] = "最低点位"
        self.mDataSpecIndexTradingDaily["pre_close"] = "昨日收盘点"
        self.mDataSpecIndexTradingDaily["change"] = "涨跌点"
        self.mDataSpecIndexTradingDaily["pct_chg"] = "涨跌幅（%）"
        self.mDataSpecIndexTradingDaily["vol"] = "成交量（手）"
        self.mDataSpecIndexTradingDaily["amount"] = "成交额（千元）"

        # stock_basic()所有A股的基础信息列
        self.mDataAllStockBasicInfo["ts_code"] = "TS代码"
        self.mDataAllStockBasicInfo["symbol"] = "股票代码"
        self.mDataAllStockBasicInfo["name"] = "股票名称"
        self.mDataAllStockBasicInfo["area"] = "所在地域"
        self.mDataAllStockBasicInfo["industry"] = "所属行业"
        self.mDataAllStockBasicInfo["fullname"] = "股票全称"
        self.mDataAllStockBasicInfo["enname"] = "英文全称"
        self.mDataAllStockBasicInfo["market"] = "市场类型（主板/中小板/创业板/科创板）"
        self.mDataAllStockBasicInfo["exchange"] = "交易所代码"
        self.mDataAllStockBasicInfo["curr_type"] = "交易货币"
        self.mDataAllStockBasicInfo["list_status"] = "上市状态"
        self.mDataAllStockBasicInfo["list_date"] = "上市日期"

        # get_today_all()股票实时数据列
        self.mDataTradingDaysMap["code"] = "代码"
        self.mDataTradingDaysMap["name"] = "名称"
        self.mDataTradingDaysMap["changepercent"] = "涨跌幅（%）"
        self.mDataTradingDaysMap["trade"] = "现价（元）"
        self.mDataTradingDaysMap["open"] = "开盘价（元）"
        self.mDataTradingDaysMap["close"] = "收盘价（元）"
        self.mDataTradingDaysMap["high"] = "最高价（元）"
        self.mDataTradingDaysMap["low"] = "最低价（元）"
        self.mDataTradingDaysMap["settlement"] = "昨日收盘价（元）"
        self.mDataTradingDaysMap["volume"] = "成交量（股）"
        self.mDataTradingDaysMap["turnoverratio"] = "换手率（%）"
        self.mDataTradingDaysMap["amount"] = "成交额"
        self.mDataTradingDaysMap["per"] = "市盈率"
        self.mDataTradingDaysMap["pb"] = "市净率"
        self.mDataTradingDaysMap["mktcap"] = "总市值（万）"
        self.mDataTradingDaysMap["nmc"] = "流通市值（万）"

        # get_hist_data()特定股票历史数据列
        self.mDataSpecStockHistory["date"] = "日期"
        self.mDataSpecStockHistory["open"] = "开盘价"
        self.mDataSpecStockHistory["high"] = "最高价"
        self.mDataSpecStockHistory["close"] = "收盘价"
        self.mDataSpecStockHistory["low"] = "最低价"
        self.mDataSpecStockHistory["volume"] = "成交量（手）"
        self.mDataSpecStockHistory["price_change"] = "价格变动"
        self.mDataSpecStockHistory["p_change"] = "涨跌幅（%）"
        self.mDataSpecStockHistory["ma5"] = "5日均价"
        self.mDataSpecStockHistory["ma10"] = "10日均价"
        self.mDataSpecStockHistory["ma20"] = "20日均价"
        self.mDataSpecStockHistory["v_ma5"] = "5日均量"
        self.mDataSpecStockHistory["v_ma10"] = "10日均量"
        self.mDataSpecStockHistory["v_ma20"] = "20日均量"
        self.mDataSpecStockHistory["turnover"] = "换手率（%）"

        # get_stock_basics()股票基本面信息列
        self.mDataCompanyBasicInfo["code"] = "代码"
        self.mDataCompanyBasicInfo["name"] = "名称"
        self.mDataCompanyBasicInfo["industry"] = "细分行业"
        self.mDataCompanyBasicInfo["area"] = "地区"
        self.mDataCompanyBasicInfo["pe"] = "市盈率"
        self.mDataCompanyBasicInfo["outstanding"] = "流通股本"
        self.mDataCompanyBasicInfo["totals"] = "总股本(万)"
        self.mDataCompanyBasicInfo["totalAssets"] = "总资产(万)"
        self.mDataCompanyBasicInfo["liquidAssets"] = "流动资产"
        self.mDataCompanyBasicInfo["fixedAssets"] = "固定资产"
        self.mDataCompanyBasicInfo["reserved"] = "公积金"
        self.mDataCompanyBasicInfo["reservedPerShare"] = "每股公积金"
        self.mDataCompanyBasicInfo["esp"] = "每股收益"
        self.mDataCompanyBasicInfo["bvps"] = "每股净资"
        self.mDataCompanyBasicInfo["pb"] = "市净率"
        self.mDataCompanyBasicInfo["timeToMarket"] = "上市日期"
        self.mDataCompanyBasicInfo["undp"] = "未分利润"
        self.mDataCompanyBasicInfo["perundp"] = "每股未分配"
        self.mDataCompanyBasicInfo["rev"] = "收入同比(%)"
        self.mDataCompanyBasicInfo["profit"] = "毛利率(%)"
        self.mDataCompanyBasicInfo["npr"] = "净利润率(%)"
        self.mDataCompanyBasicInfo["holders"] = "股东人数"

        # pro.stock_company()上市公司基本面信息列
        self.mDataStockCompany["ts_code"] = "股票代码"
        self.mDataStockCompany["exchange"] = "交易所代码"
        self.mDataStockCompany["chairman"] = "法人代表"
        self.mDataStockCompany["manager"] = "总经理"
        self.mDataStockCompany["secretary"] = "董秘"
        self.mDataStockCompany["reg_capital"] = "注册资本"
        self.mDataStockCompany["setup_date"] = "注册日期"
        self.mDataStockCompany["province"] = "所在省份"
        self.mDataStockCompany["city"] = "所在城市"
        self.mDataStockCompany["introduction"] = "公司介绍"
        self.mDataStockCompany["website"] = "公司主页"
        self.mDataStockCompany["email"] = "电子邮件"
        self.mDataStockCompany["office"] = "办公室"
        self.mDataStockCompany["employees"] = "员工人数"
        self.mDataStockCompany["main_business"] = "主要业务及产品"
        self.mDataStockCompany["business_scope"] = "经营范围"

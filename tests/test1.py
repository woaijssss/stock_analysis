
import tushare
from pandas import DataFrame
import pandas as pd

dataColumnsMap = {
	"code":			"代码",
	"name": 			"名称",
	"changepercent": 	"涨跌幅（%）",
	"trade": 			"现价（元）",
	"open": 			"开盘价（元）",
	"high": 			"最高价（元）",
	"low": 				"最低价（元）",
	"settlement": 		"昨日收盘价（元）",
	"volume": 			"成交量（股）",
	"turnoverratio": 	"换手率（%）",
	"amount": 			"成交额",
	"per": 				"市盈率",
	"pb": 				"市净率",
	"mktcap": 			"总市值（万）",
	"nmc": 				"流通市值（万）"
}

# 获取股票当日数据
df = tushare.get_today_all()

for name in list(df.columns):
    if name in dataColumnsMap:
        df.rename(columns={name:dataColumnsMap[name]}, inplace = True)  # 修改列名

df.to_excel("../datas/test1.xlsx", sheet_name='Sheet1')

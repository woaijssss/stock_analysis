
import tushare
from stock_analysis.auxiliary_lib.NounsEng2Chn import NounsEng2Chn
from pandas import DataFrame
import pandas as pd

# 获取股票当日数据
df = tushare.get_today_all()

for name in list(df.columns):
    if name in NounsEng2Chn().getDataMap():
        df.rename(columns={name:NounsEng2Chn().getDataMap()[name]}, inplace = True)  # 修改列名

df.to_excel("../datas/股票实时数据.xlsx", sheet_name='股票实时信息')

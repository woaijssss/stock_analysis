
import tushare
from stock_analysis.auxiliary_lib.NounsEng2Chn import NounsEng2Chn

# 获取指定股票历史数据

code = "000799"
df = tushare.get_hist_data(code, start='1970-01-01')
for name in list(df.columns):
    if name in NounsEng2Chn().getDataMap():
        df.rename(columns={name:NounsEng2Chn().getDataMap()[name]}, inplace = True)  # 修改列名

df.to_excel("../datas/历史数据/" + code + "历史数据.xlsx", sheet_name='股票历史信息')

import tushare
from stock_analysis.auxiliary_lib.NounsEng2Chn import NounsEng2Chn

pro = tushare.pro_api(token='063c3e42ec30996bf395ddb0b7875918b2280544dee0c7e657b8136d')
#查询当前所有正常上市交易的股票列表

df = pro.stostock_companyck_basic(exchange='', list_status='L')
df.to_excel("../datas/当前上市交易的股票列表.xlsx", sheet_name='股票列表')


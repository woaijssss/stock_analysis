import sys
import os
from pathlib import Path
import pandas as pd
from pandas import DataFrame
import tushare as ts
sys.path.append(os.path.abspath('..'))
from auxiliary_lib.NounsEng2Chn import NounsEng2Chn

pro = ts.pro_api(token='e5ccd9b1da858f2e127afef26431dd550ebd8d837f2394816722f0f9')

root_path = "./datas/"
stock_info_file = "A_当前上市交易的股票列表.xlsx"

dataPath = Path(root_path)
if not dataPath.is_dir():  # datas目录不存在，则创建（因git不上传数据文件，因此git clone之后没有datas目录）
    dataPath.mkdir()

df_StockInfo = None
if stock_info_file in os.listdir(root_path):    # 文件存在
    print(stock_info_file, "存在")
    df_StockInfo = pd.read_excel(root_path + stock_info_file, sheet_name='股票列表')
else:
    df_StockInfo = pro.stock_basic(list_status='L', fields='ts_code,symbol,name,area,industry,market,list_date,list_status,exchange,fullname,enname,curr_type')
    df_StockInfo = NounsEng2Chn().converseEng2Chn(df_StockInfo, NounsEng2Chn.mDataAllStockBasicInfo)
    df_StockInfo.to_excel(root_path + stock_info_file, sheet_name='股票列表', index=False)

compony_basic_file = "上市公司基本信息.xlsx"
df_company_basic = None
if compony_basic_file in os.listdir("./datas"):    # 文件存在
    print(compony_basic_file, "存在")
    df_company_basic = pd.read_excel(root_path + compony_basic_file, sheet_name='公司信息')

else:
    columns = "ts_code,exchange,chairman,manager,secretary,reg_capital,setup_date,province,city,introduction,website,email,office,employees,main_business,business_scope"
    df_company_basic = pro.stock_company(fields=columns)
    df_company_basic = NounsEng2Chn().converseEng2Chn(df_company_basic, NounsEng2Chn.mDataStockCompany)
    df_company_basic.to_excel(root_path + compony_basic_file, sheet_name='公司信息', index=False)

company_datas_file = "上市公司运营数据信息.xlsx"
df_company_datas = None
if company_datas_file in os.listdir("./datas"):    # 文件存在
    print(stock_info_file, "存在")
    df_company_datas = pd.read_excel(root_path + company_datas_file, sheet_name='公司数据信息')
else:
    df_company_datas = ts.get_stock_basics()
    # print(df_company_datas.columns)
    df_company_datas = NounsEng2Chn().converseEng2Chn(df_company_datas, NounsEng2Chn.mDataCompanyBasicInfo)
    # print(df_company_datas.columns)
    df_company_datas.to_excel(root_path + company_datas_file, sheet_name='公司数据信息', index=False)



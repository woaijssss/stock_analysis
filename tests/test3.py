import pandas as pd
import mplfinance as mpf

'''
    mplfinance详解
    https://blog.csdn.net/wuwei_201/article/details/105781844
'''

df = pd.read_excel('../datas/股票数据/603703盛洋科技.xlsx', sheet_name='历史日K数据', index_col=0, parse_dates=True)
df.index.name = 'Date'

# my_color = mpf.make_marketcolors(up='cyan', down='red', edge='black', wick='black', volume='blue')
# my_style = mpf.make_mpf_style(marketcolors=my_color, gridaxis='both', gridstyle='-.', y_on_right=True)
mpf.plot(df, type='candle', style='charles', mav=(2, 5, 10), volume=True)
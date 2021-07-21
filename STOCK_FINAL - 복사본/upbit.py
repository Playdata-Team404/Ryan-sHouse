import pyupbit
import pandas as pd
import datetime
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


# tickers = pyupbit.get_tickers()
# # print(tickers)
# now = datetime.datetime.now()
# nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
# # print(nowDatetime)
# # df = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", to=nowDatetime)
# df = pyupbit.get_ohlcv("KRW-ETH", interval='hour1', count=1000)
# # df[["close", "volume"]].plot(secondary_y=["close"])
# df["close"].plot()
# plt.show()
# print(df)
# price_KRW = pyupbit.get_current_price(["KRW-BTC", "KRW-ETH", "KRW-XRP",'KRW-ETC','KRW-DOGE','KRW-AXS'])
# price_KRW = pyupbit.get_current_price(["KRW-BTC"])

# print(int(price_KRW['KRW-BTC']))
# print("\nBTC : {0:>10,} 원".format(int(price_KRW["KRW-BTC"]))) # 딕셔너리 type
# print("ETH : {0:>10,} 원".format(int(price_KRW["KRW-ETH"])))
# print("XRP : {0:>10,} 원".format(int(price_KRW["KRW-XRP"])))
# print("ETC : {0:>10,} 원".format(int(price_KRW["KRW-ETC"])))
# print("DOGE : {0:>10,} 원".format(int(price_KRW['KRW-DOGE'])))
# print("AXS : {0:>10,} 원".format(int(price_KRW["KRW-AXS"])))
# print("ETC : {0:>10,} 원".format(int(price_KRW["KRW-ETC"])))
# print("ETC : {0:>10,} 원".format(int(price_KRW["KRW-ETC"])))
# print("ETC : {0:>10,} 원".format(int(price_KRW["KRW-ETC"])))
# print(price_KRW)

'''
비트코인
이더리움
리플
이클
도지
엑시인피니티
샌드박스
넴
리스크
밀크

,'KRW-ETC','KRW-DOGE','KRW-AXS','KRW-SAND','KRW-XEM','KRW-LSK','KRW-MLK'

'''


df = pyupbit.get_ohlcv("KRW-TRX", interval='day', count=1000)
# print(df)
ma5 = df['close'].rolling(window=5).mean() 
ma10 = df['close'].rolling(window=10).mean()
ma5 = ma5.reset_index()
ma10 = ma10.reset_index()
fig = go.Figure()
fig.add_trace(
    go.Scatter(x=ma5['index'], y=ma5['close'],
              name='이동평균선 5일')
)
fig.add_trace(
    go.Scatter(x=ma10['index'], y=ma10['close'],
              name='이동평균선 10일')
)
fig.update_layout(
    title_text = '종가기준 이동평균선 시각화',
    yaxis_tickformat = ','
)
fig.show()


# plt.rcParams["figure.figsize"] = (12,6)
# plt.rcParams["axes.formatter.limits"] = -10000, 10000
# # df = pyupbit.get_ohlcv("KRW-BTC")
# # print(df)

# # 가격 차트 그리기
# df = pyupbit.get_ohlcv("KRW-TRX", interval='day', count=100)
# # print("\n---BTC 가격---")
# # print(df)
# # df.head(10)

# df["close"].plot()
# # df["close"].plot()
# plt.show()
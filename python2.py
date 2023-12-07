import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
import datetime
import pmdarima as pm
import seaborn as sns
sns.set()

start_date = datetime.datetime(2018, 1, 1)
end_date = datetime.datetime.now()
df = yf.download(tickers="AAPL", start= start_date, end= end_date)
df.head()
print(df.tail())

plt.plot(df['Close'])
df['Close'].rolling(window=20).mean().plot()
df['Open'].rolling(window=20).mean().plot()
plt.title('Giá đóng/mở cửa của APPLE')
plt.xlabel('Năm')
plt.ylabel('Giá')
plt.legend()
plt.grid(True)
plt.show()

df['Close'].rolling(window=30).mean().plot(label='MA30')
plt.title('Biểu đồ đường trung bình động MA30')
plt.xlabel('Năm')
plt.ylabel('Giá')
plt.legend()
plt.grid(True)
plt.show()

df['50_SMA'] = df['Close'].rolling(50).mean().plot(label='50_SMA')
df['200_SMA'] = df['Close'].rolling(200).mean().plot(label='200_SMA')
plt.title('Biểu đồ đường trung bình động đơn giản SMA50 và SMA200 ')
plt.xlabel('Năm')
plt.ylabel('Giá')
plt.legend()
plt.grid(True)
plt.show()

fig = go.Figure()
fig.add_trace(go.Candlestick(
                            x=df.index,
                            open=df['Open'],
                            high=df['High'],
                            low=df['Low'],
                            close=df['Close'],
                            ))
df['30MA'] = df['Close'].rolling(window=30).mean()
df['50MA'] = df['Close'].rolling(window=50).mean()
fig.add_trace(go.Scatter(x=df.index, y=df['30MA'],name='30MA'))
fig.add_trace(go.Scatter(x=df.index, y=df['50MA'],name='50MA'))
fig.update_layout( title= 'Biểu đồ chứng khoán APPLE')
fig.update_layout(xaxis_title ='Năm' )
fig.update_layout(yaxis_title ='Giá' )
fig.show()

delta = df['Adj Close'].diff(1)
delta.dropna(inplace=True)
positive = delta.copy()
negative = delta.copy()
positive[positive <0] = 0
negative[negative >0] = 0
days = 14
average_gain = positive.rolling(window=days).mean()
average_loss = abs(negative.rolling(window=days).mean())
relative_strength = average_gain / average_loss
RSI = 100.0 - (100.0/(1.0 + relative_strength))
combined = pd.DataFrame()
combined['Adj Close'] = df['Adj Close']
combined['RSI'] = RSI

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(combined.index, combined['Adj Close'], color='lightgray')
ax1.set_title("Adjusted Close Price", color='white')
ax1.grid(True, color='#555555')
ax1.set_axisbelow(True)
ax1.set_facecolor('black')
ax1.figure.set_facecolor('#121212')
ax1.tick_params(axis='x', colors='white')
ax1.tick_params(axis='y', colors='white')

ax2 = plt.subplot(212, sharex=ax1)
ax2.plot(combined.index, combined [ 'RSI'], color='lightgray')
ax2.axhline(0, linestyle='--', alpha=0.5, color='#ff0000')
ax2.axhline(10, linestyle='--', alpha=0.5, color='#ffaa00')
ax2.axhline(20, linestyle='--', alpha=0.5, color='#00ff00')
ax2.axhline(30, linestyle='--', alpha=0.5, color='#cccccc')
ax2.axhline(70, linestyle='--', alpha=0.5, color='#cccccc')
ax2.axhline(80, linestyle='--', alpha=0.5, color='#00ff00')
ax2.axhline(90, linestyle='--', alpha=0.5, color='#ffaa00')
ax2.axhline(100, linestyle='--', alpha=0.5, color='#ff0000')

ax2.set_title("RSI Value")
ax2.grid(False)
ax2.set_axisbelow (True)
ax2.set_facecolor('black')
ax2.tick_params (axis='x', colors='white')
ax2.tick_params (axis='y', colors='white')
plt.show()



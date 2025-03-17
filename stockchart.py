import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import matplotlib.pyplot as plt
# from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go 
import base64


# Input from sidebar
ticker = st.sidebar.text_input('Code Saham', 'BBCA.JK')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')
# Download stock data from Yahoo Finance
data = yf.download(ticker, start=start_date, end=end_date)

# Reset index (just in case)
data = data.reset_index()
data.columns = data.columns.droplevel(1)

# Display data summary
st.subheader(f'Stock Data From {start_date} To {end_date}')
st.write(data) 

# Closing Price vs Time Chart with 100MA
st.subheader('Closing Price vs Time Chart with 100MA')
ma100 = data['Close'].rolling(100).mean()
fig = plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['Close'], label='Close Price', color='blue')
plt.plot(data['Date'], ma100, label='100-Day Moving Average', color='red')
plt.title(f'{ticker} Closing Price and 100-Day MA')
plt.legend(loc='best')
st.pyplot(fig)

# Closing Price vs Time Chart with 200MA
st.subheader('Closing Price vs Time Chart with 200MA')
ma200 = data['Close'].rolling(200).mean()
fig = plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['Close'], label='Close Price', color='blue')
plt.plot(data['Date'], ma100, label='100-Day Moving Average', color='red')
plt.plot(data['Date'], ma200, label='200-Day Moving Average', color='green')
plt.title(f'{ticker} Closing Price, 100-Day and 200-Day MAs')
plt.legend(loc='best')
st.pyplot(fig)

# Candlestick
data_candle = yf.download(ticker, start = start_date, end = end_date, interval="1d")
data_candle = data_candle.reset_index()  # Reset index agar 'Date' menjadi kolom biasa
data_candle.columns = data_candle.columns.droplevel(1)

# Candlestick Chart
st.subheader(f'Candlestick Chart ({start_date}) - ({end_date})')

fig_candle = go.Figure(
    data=[
        go.Candlestick(
            x=data_candle['Date'],
            open=data_candle['Open'],
            high=data_candle['High'],
            low=data_candle['Low'],
            close=data_candle['Close'],
            name='Candlestick'
        )
    ]
)

fig_candle.update_layout(
    title=f'{ticker} Candlestick Chart ({start_date}) - ({end_date})',
    xaxis_title='Date',
    yaxis_title='Price',
    xaxis_rangeslider_visible=False
)

# Tampilkan chart di Streamlit
st.plotly_chart(fig_candle)

# RSI Chart
st.subheader('Relative Strength Index (RSI)')
def compute_rsi(data, window=14):
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

data['RSI'] = compute_rsi(data)
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(x=data['Date'], y=data['RSI'], mode='lines', name='RSI'))
fig_rsi.add_hline(y=70, line_dash='dash', line_color='red', annotation_text='Overbought')
fig_rsi.add_hline(y=30, line_dash='dash', line_color='green', annotation_text='Oversold')
fig_rsi.update_layout(title='RSI Chart', xaxis_title='Date', yaxis_title='RSI Value')
st.plotly_chart(fig_rsi)

# Bollinger Bands Chart
st.subheader('Bollinger Bands')
window = 20  # 20-day moving average
std_dev = 2  # Standard deviation multiplier
ma = data['Close'].rolling(window).mean()
std = data['Close'].rolling(window).std()
upper_band = ma + (std_dev * std)
lower_band = ma - (std_dev * std)

fig_bb = go.Figure()
fig_bb.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close Price'))
fig_bb.add_trace(go.Scatter(x=data['Date'], y=upper_band, mode='lines', name='Upper Band', line=dict(color='red')))
fig_bb.add_trace(go.Scatter(x=data['Date'], y=lower_band, mode='lines', name='Lower Band', line=dict(color='green')))
fig_bb.update_layout(title='Bollinger Bands', xaxis_title='Date', yaxis_title='Price')
st.plotly_chart(fig_bb)

import yfinance as yf
import streamlit as st

st.write("""
# Simple Stock Price App

Shown are the stock closing price and volumn of Google!

""")
#define the ticker symbol
tickerSymbol = 'GOOGL'

#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

#get the historical prices for the ticker
tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2021-5-31')

st.write("""
# Closing price
""")
st.line_chart(tickerDf.Close)
st.write("""
# Volume price
""")
st.line_chart(tickerDf.Volume)
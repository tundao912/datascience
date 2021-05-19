import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
from PIL import Image
from bs4 import BeautifulSoup
import requests
import json
import time

st.set_page_config(layout='wide')

image = Image.open('dna-logo.jpeg')
st.image(image, width=500)

st.title('Crypto Price App')
st.markdown("""
This app retrieves cryptocurrency prices for the top 100 cryptocurrencies (from wikipedia) and its corresponding stock closing price (year-to-date)

""")

#About
expander_bar = st.beta_expander('About')
expander_bar.markdown("""
* **Python libs:** base64, pandas, streamlit
* **Data source:** [CoinMarketCap](https://coinmarketcap.com).
""")

#Sidebar + Main panel
col1 = st.sidebar
col2, col3 = st.beta_columns((2,1))

col1.header('User Input Features')
currency_unit = col1.selectbox('Select currency for price', ('USD', 'BTC', 'ETH'))

#Web scraping data
@st.cache(suppress_st_warning=True)
def load_data():
    cmc = requests.get('https://coinmarketcap.com')
    soup = BeautifulSoup(cmc.content, 'html.parser')
    data = soup.find('script',id='__NEXT_DATA__',type='application/json')
    coins = {}

    coin_data = json.loads(data.contents[0])
    listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
    for i in listings:
        coins[str(i['id'])] = i['slug']

    coin_name = []
    coin_symbol = []
    market_cap = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []
    price = []
    volume_24h= []

    for i in listings:
        coin_name.append(i['slug'])
        coin_symbol.append(i['symbol'])
        price.append(i['quote'][currency_unit]['price'])
        percent_change_1h.append(i['quote'][currency_unit]['percentChange1h'])
        percent_change_24h.append(i['quote'][currency_unit]['percentChange24h'])
        percent_change_7d.append(i['quote'][currency_unit]['percentChange7d'])
        market_cap.append(i['quote'][currency_unit]['marketCap'])
        volume_24h.append(i['quote'][currency_unit]['volume24h'])

    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap','volumn_24h', 'price', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percent_change_1h'] = percent_change_1h
    df['percent_change_24h'] = percent_change_24h
    df['percent_change_7d'] = percent_change_7d
    df['market_cap'] = market_cap
    df['volume_24h'] = volume_24h

    return df
df = load_data()

sorted_coin = sorted(df['coin_symbol'])
selected_coin = col1.multiselect('Crytocurrency', sorted_coin, sorted_coin)
df_selected_coin = df[ (df['coin_symbol'].isin(selected_coin)) ]

num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
df_coins = df_selected_coin[:num_coin]

percent_timeframe = col1.selectbox('Percent change time frame', ['7d','24h','1h'])
percent_dict = {'7d':'percent_change_7d',
                '24h':'percent_change_24h',
                '1h':'percent_change_1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]

sort_values = col1.selectbox('Sort values? ', ['Yes', 'No'])

col2.subheader('Price Data of Selected Crytocurrency')
col2.write('Data Dimension: ' + str(df_coins.shape[0]) + ' rows and ' + str(df_coins.shape[1]) + ' columns')
col2.dataframe(df_coins)

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV file</a>'
    return href
st.markdown(filedownload(df_coins), unsafe_allow_html=True)
st.set_option('deprecation.showPyplotGlobalUse', False)

col2.subheader('Table of % Price Change')
df_change = pd.concat([df_coins.coin_symbol, df_coins.percent_change_1h, df_coins.percent_change_24h, df_coins.percent_change_7d], axis=1)
df_change = df_change.set_index('coin_symbol')
df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0

col2.dataframe(df_change)

col3.subheader('Bar plot of % Price Change')

time_frame = percent_dict.get(percent_timeframe)
if sort_values == 'Yes':
    df_change = df_change.sort_values(by=[time_frame])
col3.write('*' + time_frame + '*')
plt.figure(figsize=(5,25))
plt.subplots_adjust(top=1, bottom=0)
df_change[time_frame].plot(kind='barh', color=df_change['positive_' + time_frame].map({True: 'g', False: 'r'}))
col3.pyplot(plt)
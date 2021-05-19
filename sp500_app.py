import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf

st.title('S&P 500 App')

st.markdown("""
This app retrieves the list of the **S&P 500** (from wikipedia) and its corresponding stock closing price (year-to-date)

* **Python libs:** base64, pandas, streamlit
* **Data source:** [Wikipedia](https://www.wikipedia.org/).
""")

st.sidebar.header('User Input Features')
@st.cache(suppress_st_warning=True)
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header=0)
    df = html[0]
    return df
df = load_data()
sector_unique = df['GICS Sector'].unique()
sector = df.groupby('GICS Sector')
sorted_sector_unique = sorted(sector_unique)
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

df_selected_sector = df[ (df['GICS Sector'].isin(selected_sector)) ]

st.header('Display Companies in Selected Sector')
st.write('Data dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns')
st.dataframe(df_selected_sector)

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="sp500.csv">Download CSV file</a>'
    return href
st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)
st.set_option('deprecation.showPyplotGlobalUse', False)

data = yf.download(
    tickers=list(df_selected_sector[:10].Symbol),
    period='ytd',
    interval='1d',
    group_by='ticker',
    auto_adjust=True,
    prepost=True
)

def price_plot(symbol):
    df2 = pd.DataFrame(data[symbol].Close)
    df2['Date'] = df2.index
    plt.fill_between(df2.Date, df2.Close, color='skyblue', alpha=0.3)
    plt.plot(df2.Date, df2.Close, color='skyblue', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight= 'bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing Price', fontweight='bold')

    return st.pyplot()

num_company = st.sidebar.slider('Number of companies: ', 1, 5)

if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)
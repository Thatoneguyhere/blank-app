import yfinance as yf
import pandas as pd
from requests.exceptions import RequestException

def load_stock_data(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end)
        if data.empty:
            return None
        data.reset_index(inplace=True)
        return data
    except RequestException:
        return None

def get_macro_data():
    try:
        url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=GDP'
        df = pd.read_csv(url)
        df['DATE'] = pd.to_datetime(df['DATE'])
        df.set_index('DATE', inplace=True)
        df.rename(columns={'GDP': 'US_GDP'}, inplace=True)
        df.fillna(method='ffill', inplace=True)
        return df
    except Exception:
        return pd.DataFrame()

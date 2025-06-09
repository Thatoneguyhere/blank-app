def add_features(data):
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['Momentum'] = data['Close'] - data['Close'].shift(10)
    data['Volatility'] = data['Close'].rolling(window=20).std()
    data['Volume_Change'] = data['Volume'].pct_change()
    data.dropna(inplace=True)
    return data

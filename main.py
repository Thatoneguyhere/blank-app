import streamlit as st
import datetime
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import pandas as pd

from config import STOCK_LIST
from data.loader import load_stock_data, get_macro_data
from data.features import add_features
from models.lstm_model import prepare_lstm_data, train_lstm_model
from analysis.sentiment import get_sentiment_score
from trading.executor import execute_trade

st.set_page_config(page_title="AI Investment Assistant", layout="wide")
st.title("📈 AI-Powered Investment Dashboard")

st.sidebar.header("Settings")
stocks = st.sidebar.multiselect("Choose stocks to monitor:", STOCK_LIST, default=["AAPL", "MSFT"])
start_date = st.sidebar.date_input("Start Date", datetime.date.today() - datetime.timedelta(days=365))
end_date = st.sidebar.date_input("End Date", datetime.date.today())

for stock in stocks:
    st.subheader(f"📊 {stock} Analysis")
    data = load_stock_data(stock, start_date, end_date)
    if data is None:
        st.warning(f"No data available for {stock}.")
        continue

    st.line_chart(data.set_index("Date")["Close"])

    headlines = [
        f"{stock} surges after earnings beat expectations",
        f"{stock} faces antitrust investigation in EU",
        f"Analysts bullish on {stock} after recent developments"
    ]
    sentiment_score = get_sentiment_score(headlines)
    sentiment_label = "🟢 Positive" if sentiment_score > 0 else "🔴 Negative" if sentiment_score < 0 else "🟡 Neutral"
    st.markdown(f"**Sentiment Score:** {sentiment_score:.2f} ({sentiment_label})")

    data = add_features(data)
    macro_data = get_macro_data()
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    df = pd.merge(data, macro_data, how='left', left_index=True, right_index=True).fillna(method='ffill')

    features = ['Close', 'MA20', 'MA50', 'Momentum', 'Volatility', 'Volume_Change', 'US_GDP']
    if len(df) < 120:
        st.info("Not enough data for forecasting.")
        continue

    X, y, scaler = prepare_lstm_data(df, features)
    model = train_lstm_model(X, y)

    last_window = X[-1].reshape(1, X.shape[1], X.shape[2])
    predicted_scaled = model.predict(last_window, verbose=0)
    reconstructed = scaler.inverse_transform(
        [[predicted_scaled[0][0]] + [0] * (len(features) - 1)]
    )
    predicted_price = reconstructed[0][0]

    st.markdown("**📈 Predicted Closing Price for Next Day:**")
    st.success(f"${predicted_price:.2f}")

    current_price = df["Close"].iloc[-1]
    trade_result = execute_trade(stock, predicted_price, current_price)
    st.info(trade_result)

    st.markdown("**🧪 Backtesting Results:**")
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = train_lstm_model(X_train, y_train)
    predicted_test_scaled = model.predict(X_test, verbose=0)

    reconstructed_pred = scaler.inverse_transform(
        [[p[0]] + [0] * (len(features) - 1) for p in predicted_test_scaled]
    )
    reconstructed_y = scaler.inverse_transform(
        [[y] + [0] * (len(features) - 1) for y in y_test]
    )

    predicted_prices = [r[0] for r in reconstructed_pred]
    actual_prices = [r[0] for r in reconstructed_y]

    fig, ax = plt.subplots()
    ax.plot(actual_prices, label="Actual")
    ax.plot(predicted_prices, label="Predicted")
    ax.legend()
    st.pyplot(fig)

    mse = mean_squared_error(actual_prices, predicted_prices)
    st.write(f"Mean Squared Error: {mse:.4f}")

# Optionally show the trade log
import os
if os.path.exists("trade_log.csv"):
    st.markdown("## 📜 Trade Log")
    trade_log_df = pd.read_csv("trade_log.csv", header=None, names=["Timestamp", "Symbol", "Action", "Quantity", "Price", "StopLoss"])
    st.dataframe(trade_log_df)
else:
    st.info("No trades logged yet.")

st.success("App loaded with forecasting, trading, stop-loss, and position checking!")

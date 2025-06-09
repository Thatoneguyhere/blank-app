import os
from dotenv import load_dotenv

load_dotenv()

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

STOCK_LIST = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
WINDOW_SIZE = 60
TRADE_STOP_LOSS_PERCENT = 0.05  # 5% stop-loss

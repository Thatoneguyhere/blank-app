import csv
from datetime import datetime

LOG_FILE = "trade_log.csv"

def log_trade(symbol, action, qty, price, stop_loss=None):
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().isoformat(),
            symbol,
            action,
            qty,
            price,
            stop_loss if stop_loss else ""
        ])

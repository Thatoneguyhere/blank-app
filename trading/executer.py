from alpaca_trade_api.rest import REST
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY, BASE_URL, TRADE_STOP_LOSS_PERCENT
from trading.logger import log_trade

api = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, BASE_URL)

def execute_trade(symbol, predicted_price, current_price):
    try:
        # Check if you already have a position
        try:
            position = api.get_position(symbol)
            has_position = float(position.qty) > 0
        except Exception:
            has_position = False
            position = None

        # Only buy if not already holding this stock
        if not has_position and predicted_price > current_price * 1.01:
            stop_price = round(current_price * (1 - TRADE_STOP_LOSS_PERCENT), 2)
            api.submit_order(
                symbol=symbol,
                qty=1,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            log_trade(symbol, "BUY", 1, current_price, stop_price)
            return f"Buy order placed for {symbol} at ${current_price:.2f}, Stop-Loss: ${stop_price:.2f}"

        # If you have a position, check for stop-loss
        if has_position and position:
            avg_entry_price = float(position.avg_entry_price)
            if current_price < avg_entry_price * (1 - TRADE_STOP_LOSS_PERCENT):
                api.submit_order(
                    symbol=symbol,
                    qty=position.qty,
                    side='sell',
                    type='market',
                    time_in_force='gtc'
                )
                log_trade(symbol, "SELL (STOP-LOSS)", position.qty, current_price)
                return f"Stop-loss triggered for {symbol} at ${current_price:.2f}"

        return f"No trade signal for {symbol}"

    except Exception as e:
        return f"Trade execution failed: {e}"

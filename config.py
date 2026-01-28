import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = -1003878459434  # update after setup

COINDCX_KEY = os.getenv("COINDCX_KEY")
COINDCX_SECRET = os.getenv("COINDCX_SECRET")

CAPITAL_USDT = float(os.getenv("CAPITAL_USDT", 5))
LEVERAGE = float(os.getenv("LEVERAGE", 5))

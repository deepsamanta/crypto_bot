import re
import math


def parse_signal(text: str):
    t = text.upper()

    # detect LONG/SHORT
    side = None
    if "BUY" in t or "LONG" in t:
        side = "buy"
    elif "SELL" in t or "SHORT" in t:
        side = "sell"

    symbol = None
    m = re.search(r'[#\$]?([A-Z]{2,6})', t)
    if m:
        symbol = m.group(1) + "USDT"

    entry = re.search(r'ENTRY[: ]+([0-9.]+)', t)
    target = re.search(r'(TP|TARGET)[: ]+([0-9.]+)', t)
    stop = re.search(r'(SL|STOP|STOPLOSS)[: ]+([0-9.]+)', t)
 
    return {
        "symbol": symbol,
        "side": side,
        "entry": float(entry.group(1)) if entry else None,
        "target": float(target.group(2)) if target else None,
        "stop": float(stop.group(2)) if stop else None
    }

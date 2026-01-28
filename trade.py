import time, hmac, hashlib, json, requests, math
from config import COINDCX_KEY, COINDCX_SECRET, LEVERAGE

TEST_MODE = False  # <--- TURN OFF TO GO LIVE

def fut_pair(symbol):
    # ETHUSDT -> B-ETH_USDT
    base = symbol.replace("USDT", "")
    return f"B-{base}_USDT"

def place_bracket(side, symbol, entry, tp, sl, qty):
    # timestamp in milliseconds
    timestamp = int(round(time.time() * 1000))
    tp =  entry+math.floor((tp-entry)/3)

    body = {
        "timestamp": timestamp,
        "order": {
            "side": "buy" if side == "buy" else "sell",
            "pair": fut_pair(symbol),
            "order_type": "limit_order",  # or "market_order"
            "price": float(entry),        # numeric
            "total_quantity": float(qty), # numeric
            "leverage": LEVERAGE,
            "notification": "email_notification",
            "time_in_force": "good_till_cancel",
            "hidden": False,
            "post_only": False,
            "take_profit_price": float(tp),
            "stop_loss_price": float(sl)
        }
    }

    if TEST_MODE:
        print("[TEST_MODE] Would send:", body)
        return "TEST_MODE"

    json_body = json.dumps(body, separators=(',', ':'))
    secret_bytes = COINDCX_SECRET.encode('utf-8')

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "X-AUTH-APIKEY": COINDCX_KEY,
        "X-AUTH-SIGNATURE": signature
    }

    url = "https://api.coindcx.com/exchange/v1/derivatives/futures/orders/create"

    r = requests.post(url, data=json_body, headers=headers)
    print("[COINDCX]", r.status_code, r.text)
    return r.json() if r.text else None

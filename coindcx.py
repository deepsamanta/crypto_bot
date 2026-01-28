import hmac
import hashlib
import base64
import json
import time
import requests

# Enter your API Key and Secret here. If you don't have one, you can generate it from the website.
key = "4a0e4ac713a58940a9baf483aec0889df018e963a9b58dfc"
secret = "1fda38b368f118c136641ae80370b4a9347601db5885e97a528b5e4e4ec68c52"


# python3
secret_bytes = bytes(secret, encoding='utf-8')
# python2


# Generating a timestamp
timeStamp = int(round(time.time() * 1000))

body = {
        "timestamp":timeStamp , # EPOCH timestamp in seconds
        "order": {
        "side": "buy", # buy OR sell
        "pair": "B-XRP_USDT", # instrument.string
        "order_type": "market_order", # market_order OR limit_order 
        "price": "1.9160", #numeric value
    # "stop_price": "0.2962", #numeric value
        "total_quantity": 4, #numerice value
        "leverage": 5, #numerice value
        "notification": "email_notification", # no_notification OR email_notification OR push_notification
        "time_in_force": "good_till_cancel", # good_till_cancel OR fill_or_kill OR immediate_or_cancel
        "hidden": False, # True or False
        "post_only": False, # True or False
    "take_profit_price": 1.950,
    "stop_loss_price": 1.90
        }
        }

json_body = json.dumps(body, separators = (',', ':'))

signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

url = "https://api.coindcx.com/exchange/v1/derivatives/futures/orders/create"

headers = {
    'Content-Type': 'application/json',
    'X-AUTH-APIKEY': key,
    'X-AUTH-SIGNATURE': signature
}

response = requests.post(url, data = json_body, headers = headers)
data = response.json()
print(data)
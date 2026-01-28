from config import CAPITAL_USDT, LEVERAGE
import math

STEP = 0.001  # default precision for majors

def apply_precision(qty, step=STEP):
    # round & floor to valid step
    qty = round(qty, 6)
    return math.floor(qty / step) * step

def compute_qty(entry_price: float):
    exposure = CAPITAL_USDT * LEVERAGE
    raw_qty = exposure / entry_price

    # If qty > 500, force integer (no decimals)
    if raw_qty > 50:
        return int(raw_qty)

    # Else keep futures precision
    return apply_precision(raw_qty)

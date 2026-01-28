from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from signal_parser import parse_signal
from trade import place_bracket
from risk import compute_qty
from config import TELEGRAM_BOT_TOKEN, CHANNEL_ID

print("[BOT] Starting...")

async def handle(update, context: ContextTypes.DEFAULT_TYPE):
    # Channel signals arrive as channel_post
    msg = update.channel_post
    if not msg:
        return

    # Extract text or caption (image based signals)
    text = msg.text or msg.caption

    # Debug logs
    print("------------------------------------------------")
    print("[RECV RAW]", msg)
    print("[CHAT ID]", msg.chat.id)

    if not text:
        print("[SKIP] Message has no text/caption (likely image only)")
        return

    print("[RECV TEXT]", text)

    # Ignore messages from channels we don't care about
    if msg.chat.id != CHANNEL_ID:
        print("[SKIP] Wrong channel:", msg.chat.id)
        return

    # Parse the signal
    data = parse_signal(text)
    print("[PARSED]", data)

    # Validate parsing
    if not all([data.get("symbol"), data.get("side"), data.get("entry"), data.get("target"), data.get("stop")]):
        print("[SKIP] Invalid / incomplete signal")
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text="⚠ Invalid signal format (missing ENTRY/TP/SL)"
        )
        return

    # Compute qty ($5 x 5 leverage = exposure)
    qty = compute_qty(data["entry"])
    print("[QTY]", qty)

    # Debug feedback to channel
    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=(
            "🧾 SIGNAL RECEIVED\n"
            f"Symbol: {data['symbol']}\n"
            f"Side: {data['side'].upper()}\n"
            f"Entry: {data['entry']}\n"
            f"TP: {data['target']}\n"
            f"SL: {data['stop']}\n"
            f"Qty: {qty}\n"
            f"Status: 📡 EXECUTING..."
        )
    )

    # Execute order
    resp = place_bracket(
        data["side"],
        data["symbol"],
        data["entry"],
        data["target"],
        data["stop"],
        qty
    )

    print("[ORDER RESPONSE]", resp)

    # Post execution result
    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=f"🚀 ORDER SENT\nResponse: {resp}"
    )

# Build application
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# Handler for ALL channel messages
app.add_handler(MessageHandler(filters.ALL, handle))

# Polling loop
app.run_polling()

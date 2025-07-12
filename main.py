import os
import requests
import telegram
from telegram.ext import Dispatcher, CommandHandler
from flask import Flask, request

# === ТВОЙ ТОКЕН БОТА ===
TOKEN = "7547829682:AAEkCr3jn5dLvPPGqafEhLYvWCLhyGUtW0E"

# === Flask и Telegram ===
app = Flask(__name__)
bot = telegram.Bot(token=TOKEN)

@app.route('/')
def home():
    return 'Bot is running!'

# === Команды ===
def start(update, context):
    update.message.reply_text("Привет! Используй команду /analyze")

def analyze(update, context):
    try:
        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=15m&limit=2"
        data = requests.get(url).json()
        open_price = float(data[-1][1])
        close_price = float(data[-1][4])
        signal = "BUY" if close_price > open_price else "SELL" if close_price < open_price else "WAIT"
        update.message.reply_text(f"{signal}\nBTCUSDT: {close_price:.2f}")
    except Exception as e:
        update.message.reply_text("Ошибка анализа")

# === Webhook обработка ===
@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

# === Dispatcher ===
from telegram.ext import Updater
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("analyze", analyze))

# === Установить Webhook ===
bot.set_webhook(f"https://<ТВОЙ-RENDER-URL>/{TOKEN}")

# === Запустить Flask ===
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

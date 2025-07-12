import logging
from flask import Flask, request
import requests
import telegram
from telegram.ext import Dispatcher, CommandHandler

# === ТВОЙ ТОКЕН ===
TOKEN = "7547829682:AAEkCr3jn5dLvPPGqafEhLYvWCLhyGUtW0E"
WEBHOOK_URL = "https://crypto-signal-bot-71sj.onrender.com"

# === Настройка Telegram бота ===
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)
dispatcher = Dispatcher(bot, None, use_context=True)

# === Команда /start ===
def start(update, context):
    update.message.reply_text("Привет! Используй /analyze чтобы получить сигнал.")

# === Команда /analyze ===
def analyze(update, context):
    try:
        symbol = "BTCUSDT"
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=15m&limit=2"
        response = requests.get(url)
        data = response.json()

        last_candle = data[-1]
        open_price = float(last_candle[1])
        close_price = float(last_candle[4])

        if close_price > open_price:
            signal = "BUY"
        elif close_price < open_price:
            signal = "SELL"
        else:
            signal = "WAIT"

        update.message.reply_text(f"{signal} — BTCUSDT: {close_price:.2f}")
    except Exception as e:
        update.message.reply_text("Ошибка при анализе.")
        logging.error(f"Ошибка: {e}")

# === Регистрируем команды ===
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("analyze", analyze))

# === Webhook endpoint ===
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

# === Устанавливаем webhook при запуске ===
@app.route('/')
def index():
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    return 'Webhook установлен'

# === Запуск Flask-сервера ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

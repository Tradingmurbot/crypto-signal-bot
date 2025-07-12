import logging
from flask import Flask, request, jsonify
import requests
import telegram
from telegram import Update
from telegram.ext import Dispatcher, CommandHandler

# === ТВОЙ ТОКЕН ===
TOKEN = "7547829682:AAEkCr3jn5dLvPPGqafEhLYvWCLhyGUtW0E"
WEBHOOK_URL = "https://crypto-signal-bot-71sj.onrender.com"

# === Настройка Telegram бота ===
bot = telegram.Bot(token=TOKEN)

# === Установка вебхука ===
bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")

# === Flask-приложение ===
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, use_context=True)

# === Команда /start ===
def start(update, context):
    update.message.reply_text("Привет! Используй команду /analyze")

# === Команда /analyze ===
def analyze(update, context):
    try:
        symbol = "BTCUSDT"
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url)
        data = response.json()
        price = data["price"]
        update.message.reply_text(f"Текущая цена BTC/USDT: {price}")
    except Exception as e:
        logging.error(e)
        update.message.reply_text("Ошибка анализа.")

# === Регистрация команд ===
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("analyze", analyze))

# === Обработка вебхука ===
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
        return jsonify({"status": "ok"})

# === Проверка живости ===
@app.route('/')
def index():
    return "Бот работает!"

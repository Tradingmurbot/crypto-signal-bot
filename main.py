import logging
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, CommandHandler

TOKEN = "ТВОЙ_ТОКЕН"
WEBHOOK_URL = "https://crypto-signal-bot-71sj.onrender.com/" + TOKEN

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, use_context=True)

# Команда /start
def start(update, context):
    update.message.reply_text("Привет! Используй команду /analyze.")

# Команда /analyze
def analyze(update, context):
    update.message.reply_text("Пока команда analyze не реализована.")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("analyze", analyze))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Бот работает!"

if __name__ == "__main__":
    app.run(debug=True)

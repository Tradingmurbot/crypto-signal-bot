import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Токен временно можно вставить вручную (или использовать переменные окружения)
TOKEN = "7547829682:AAEkCr3jn5dLvPPGqafEhLYvWCLhyGUtW0E"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("🤖 Привет! Я крипто-бот. Ожидайте сигналов...")

def ping(update: Update, context: CallbackContext):
    update.message.reply_text("🏓 Понг!")

def analyze(update: Update, context: CallbackContext):
    try:
        # Получаем текущую цену BTC с Binance
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url).json()
        price = float(response["price"])

        # Простейшая логика: Buy / Sell / Wait
        if price < 60000:
            signal = "🟢 BUY"
        elif price > 64000:
            signal = "🔴 SELL"
        else:
            signal = "🟡 WAIT"

        update.message.reply_text(f"📊 Цена BTC: ${price:.2f}\n📈 Сигнал: {signal}")
    except Exception as e:
        update.message.reply_text(f"❌ Ошибка: {str(e)}")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("ping", ping))
    dispatcher.add_handler(CommandHandler("analyze", analyze))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

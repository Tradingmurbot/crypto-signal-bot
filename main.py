import requests
from telegram.ext import Updater, CommandHandler
import logging

# === ТВОЙ ТОКЕН ===
TOKEN = "7547829682:AAEkCr3jn5dLvPPGqafEhLYvWCLhyGUtW0E"

# === Логирование (для Render) ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# === Логика анализа ===
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

        update.message.reply_text(f"{signal}\nBTCUSDT: {close_price:.2f}")
    except Exception as e:
        update.message.reply_text("Ошибка анализа.")
        logging.error(f"Ошибка: {e}")

# === Стартовая команда ===
def start(update, context):
    update.message.reply_text("Привет! Используй команду /analyze")

# === Основной цикл ===
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("analyze", analyze))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

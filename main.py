import os
from telegram import Bot, Update
from telegram.ext import CommandHandler, Updater

TOKEN = "7547829682:AAEkCr3jn5dLvPPGqafEhLYvWCLhyGUtW0E"

def start(update, context):
    update.message.reply_text("🤖 Привет! Я крипто-бот. Ожидайте сигналов...")

def ping(update, context):
    update.message.reply_text("🏓 Pong!")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ping", ping))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

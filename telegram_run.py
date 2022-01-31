import telegram
from config import token_telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from main_full import main

bot = telegram.Bot(token=token_telegram)
updater = Updater(token=token_telegram, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Формирую пост Космонавтов 19')
    main(update, context)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Пост вк готов и опубликован')



if __name__ == "__main__":
    start_headler = CommandHandler('start', start)
    dispatcher.add_handler(start_headler)
    updater.start_polling()

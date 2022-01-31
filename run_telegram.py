# Done! Congratulations on your new bot. You will find it at t.me/pobeda_post_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.
#
# Use this token to access the HTTP API:
# 5248571053:AAEVLqq2bpYnKyAQ1tPGJ_wDdr3mhcqrdpk
# Keep your token secure and store it safely, it can be used by anyone to control your bot.
#
# For a description of the Bot API, see this page: https://core.telegram.org/bots/api


import telegram
from config import token_telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from main_full import main

bot = telegram.Bot(token=token_telegram)

updater = Updater(token=token_telegram,use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Пост вк готов')

start_headler = CommandHandler('start',start)
dispatcher.add_handler(start_headler)
updater.start_polling()
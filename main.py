#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import traceback
from telegram import *
from telegram.ext import *
from chatgpt3 import ChatGPT3
from dotenv import load_dotenv
import helpers
load_dotenv()


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = gpt3.talk(text)
    update.message.reply_text(response)


def search_game_all(update, context):
    game = (' ').join(i for i in context.args[:])
    update.message.reply_text(f"Searching for {game} ...")
    summary = helpers.search_game_all(game)
    update.message.reply_text(summary)


def error_message(update, context):
    print(f"Update {update} caused error {context.error}")
    update.message.reply_text(f"Oops, there is an error: {context.error}")


def main():

    updater = Updater(os.getenv("BOT_API_KEY"), use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("search_game_all", search_game_all))

    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error_message)

    updater.start_polling()
    updater.idle()


if __name__=="__main__":

    print("Bot has started ...")
    gpt3 = ChatGPT3(os.getenv("CHATPGT_SECRET_KEY"))
    main()

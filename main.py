#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import traceback
from telegram import *
from telegram.ext import *
from dotenv import load_dotenv
import openai
import helpers
load_dotenv()

openai.api_key = os.getenv("CHATGPT_SECRET_KEY")


def chatgpt_response(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )

    return response['choices'][0]['message']['content']


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = chatgpt_response(text)
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
    main()

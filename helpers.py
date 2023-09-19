#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import gspread
import traceback
import pandas as pd
from dotenv import load_dotenv
from gspread_dataframe import get_as_dataframe
load_dotenv()


gc = gspread.service_account(filename=os.getenv("CREDENTIALS_FILE"))
sh = gc.open_by_key(os.getenv("SPREADSHEET_KEY"))
gamepass_sheet = sh.worksheet(os.getenv("GAMEPASS_SHEET"))
game_libraries_sheet = sh.worksheet(os.getenv("GAME_LIBRARIES_SHEET"))


def search_game_all(game):

    # base text
    text = f"Game : {game}\n"

    # get data from google sheet
    gamepass = get_as_dataframe(gamepass_sheet)
    gamepass = gamepass.astype(str).apply(lambda x: x.str.lower())

    try:
        # check if game is available on Game Pass Console
        console = [i for i in gamepass['Console Games'].tolist() if game in i]
        # check if game will available on Game Pass
        soon = [i for i in gamepass['Coming Soon'].tolist() if game in i]

        if len(console) > 0 and len(soon) > 0:
            text += "\n* Game Pass: \n - " + '\n - '.join(console)
            text += "\n\n* Coming on Game Pass: \n - " + '\n - '.join(soon)
        elif len(console) > 0 and len(soon) == 0:
            text += "\n* Game Pass: \n - " + '\n - '.join(console)
        elif len(console) == 0 and len(soon) > 0:
            text += "\n* Game Pass: Not available\n"
            text += "\n* Coming on Game Pass: \n - " + '\n - '.join(soon)
        else:
            text += "\n* Game Pass : Not available\n"
            text += "\n* Coming on Game Pass : Not soon\n"

    except Exception as e:
        print(traceback.format_exc())
        return "Oops, there is an error: " + str(e)

    return text


def game_picker():

    # get data from google sheet
    game_libraries = get_as_dataframe(game_libraries_sheet)
    game_libraries.dropna(how='all', inplace=True)
    game_libraries = game_libraries.loc[:,~game_libraries.columns.str.match("Unnamed")]
    game_libraries = game_libraries[game_libraries['Is Finished'] != 'Finished']

    # random pick game
    game = game_libraries.sample()

    return str(game.to_dict('records')[0])
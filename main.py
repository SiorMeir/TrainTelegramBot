import os
import telebot
import requests
import logging
from handlers import handle_get_current_trains
import json
from dotenv import load_dotenv

load_dotenv(".dev.env")
BOT_API_KEY = os.getenv("BOT_API_KEY")
URL = os.getenv("URL")

logger = logging.getLogger("TrainLogger")
bot = telebot.TeleBot(BOT_API_KEY)


@bot.message_handler(commands=["help"])
def get_current_trains(message):
    logger.info("Got Help requesst")
    answer = "Hey there, there's no help coming your way"  # TODO: add help
    bot.reply_to(message, answer)


@bot.message_handler(commands=["toWork"])
def get_current_trains(message):
    command = message.text.split()
    match len(command):
        case 0:  # ""
            answer = "Didn't get any commands"  # should not happen
            bot.reply_to(message, "Didn't get any commands!")
        case 1:  # "/toWork"
            answer = handle_get_current_trains(URL, "toWork")
        case 2:  # "/toWork 5"
            answer = handle_get_current_trains(URL, "toWork", time=command[1])
        case 3:  # "/toWork 5 hours"
            answer = handle_get_current_trains(
                URL, "toWork", time=command[1], units=command[2]
            )
    bot.reply_to(message, answer)


@bot.message_handler(commands=["toHome"])
def get_current_trains(message):
    logger.info("Got toWork request")
    answer = handle_get_current_trains()
    bot.reply_to(message, answer)


bot.infinity_polling()

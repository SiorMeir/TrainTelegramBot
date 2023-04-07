import os
import telebot
import requests
import logging
from handlers import handle_command_options
from logic import handle_get_current_trains
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
    answer = handle_command_options(message)
    bot.reply_to(message, answer)
    return answer


@bot.message_handler(commands=["toHome"])
def get_current_trains(message):
    logger.info("Got toWork request")
    answer = handle_get_current_trains()
    bot.reply_to(message, answer)


bot.infinity_polling()

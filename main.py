import os
import telebot
import requests
import logging
from handlers import handle_get_current_trains
import json
from dotenv import load_dotenv

load_dotenv(".dev.env")
BOT_API_KEY = os.getenv("BOT_API_KEY")
ISRAEL_TRAIN_API = "https://www.rail.co.il/apiinfo/api/infor/GetStationsInfor?stations=1400&stations=4600"

logger = logging.getLogger("TrainLogger")
bot = telebot.TeleBot(BOT_API_KEY)


@bot.message_handler(commands=["help"])
def get_current_trains(message):
    logger.info("Got Help requesst")
    answer = "Hey there, there's no help coming your way"  # TODO: add help
    bot.reply_to(message, answer)


@bot.message_handler(commands=["toWork"])
def get_current_trains(message):
    try:
        _, period, type = message.text.split()
    except ValueError as e:
        bot.reply_to(message, "Your request is not clear...")
    logger.info("Got toWork request")
    answer = handle_get_current_trains("toWork")
    bot.reply_to(message, answer)


@bot.message_handler(commands=["toHome"])
def get_current_trains(message):
    logger.info("Got toWork request")
    answer = handle_get_current_trains()
    bot.reply_to(message, answer)


bot.infinity_polling()

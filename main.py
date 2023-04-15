import os
import telebot
import requests
import logging
from handlers import handle_command_options
from logic import handle_get_current_trains
from dotenv import load_dotenv
from constants import BOT_API_KEY


load_dotenv(".dev.env")
logger = logging.getLogger(__name__)
bot = telebot.TeleBot(BOT_API_KEY)


@bot.message_handler(commands=["help"])
def get_current_trains(message):
    logger.info("Got Help requesst")
    answer = "Hey there, there's no help coming your way"  # TODO: add help
    bot.reply_to(message, answer)


@bot.message_handler(commands=["toWork"])
def get_current_trains(message):
    logger.info("Got toWork request")
    answer = handle_command_options(message, mode="toWork")
    bot.reply_to(message, answer)
    return answer


@bot.message_handler(commands=["toHome"])
def get_current_trains(message):
    logger.info("Got toHome request")
    answer = handle_get_current_trains()
    bot.reply_to(message, answer)


bot.infinity_polling()

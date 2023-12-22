import os
import telebot
from telebot import types
import requests
import logging
from handlers import handle_command_options
from logic import handle_get_current_trains
from constants import BOT_API_KEY, AVAILABLE_STATIONS

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(BOT_API_KEY)


@bot.message_handler(commands=["help"])
def get_current_trains(message):
    logger.info("Got Help requesst")
    answer = "Hey there, there's no help coming your way"  # TODO: add help
    bot.reply_to(message, answer)


# --- config commands ---


@bot.message_handler(commands=["setHome"])
def get_current_trains(message):
    logger.info("Got set home station request")
    markup = types.InlineKeyboardMarkup()
    for station in AVAILABLE_STATIONS:
        item = types.InlineKeyboardButton(
            text=station["name"], callback_data=station["id"]
        )
        markup.add(item)
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)
    # return


@bot.message_handler(commands=["setWork"])
def get_current_trains(message):
    logger.info("Got work station request")
    answer = handle_command_options(message, mode="toWork")
    bot.reply_to(message, answer)
    return answer


# --- information commands ---
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

import os
from dotenv import load_dotenv

load_dotenv(".dev.env")

BOT_API_KEY = os.getenv("BOT_API_KEY")
URL = os.getenv("URL")
HOME_STATION = os.getenv("HOME_STATION")
WORK_STATION = os.getenv("WORK_STATION")
ENV = os.getenv("ENV")

import os
from dotenv import load_dotenv


ENV = os.getenv("ENV")
if (
    ENV == "development"
):  # if env is prod, environment variables are loaded through docker
    load_dotenv(".dev.env")
BOT_API_KEY = os.getenv("BOT_API_KEY")
URL = os.getenv("URL")
HOME_STATION = os.getenv("HOME_STATION")
WORK_STATION = os.getenv("WORK_STATION")

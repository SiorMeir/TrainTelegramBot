import os
import json
from dotenv import load_dotenv

if (
    os.getenv("ENV") == "development"
):  # if env is prod, environment variables are loaded through docker
    load_dotenv(".dev.env")
BOT_API_KEY = os.getenv("BOT_API_KEY")
URL = os.getenv("URL")

STATIONS = {"home": 1400, "work": 3700}

with open("./utils/stations.json", "r") as f:
    AVAILABLE_STATIONS = json.loads(f.read())

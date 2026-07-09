from dotenv import load_dotenv

import os

load_dotenv()

class Config:

    APP_NAME = os.getenv("APP_NAME")

    APP_ENV = os.getenv("APP_ENV")

    APP_HOST = os.getenv("APP_HOST")

    APP_PORT = int(os.getenv("APP_PORT"))

    DEBUG = os.getenv("DEBUG") == "True"

    API_TOKEN = os.getenv("API_TOKEN")

    SMPP_HOST = os.getenv("SMPP_HOST")

    SMPP_PORT = int(os.getenv("SMPP_PORT"))

    SMPP_SYSTEM_ID = os.getenv("SMPP_SYSTEM_ID")

    SMPP_PASSWORD = os.getenv("SMPP_PASSWORD")

    SMPP_SOURCE_ADDR = os.getenv("SMPP_SOURCE_ADDR")

    LOG_LEVEL = os.getenv("LOG_LEVEL")
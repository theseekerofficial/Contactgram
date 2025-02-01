import os
import sys
from loguru import logger
from dotenv import load_dotenv

load_dotenv('settings.env')

env_dict = {
    "BOT_TOKEN": os.getenv("BOT_TOKEN", None),
    "BOT_ID": int(os.getenv("BOT_TOKEN", None).split(':')[0]),
    "MONGO_URI": os.getenv("MONGO_URI", None),
    "BOT_NAME": os.getenv("BOT_NAME", "Contactgram Bot"),
    "ADMIN_TEAM": os.getenv("ADMIN_TEAM", None).split(','),
    "TIMEZONE": os.getenv("TIMEZONE", "Asia/Colombo"),
    "AUTO_CONFIG": os.getenv("AUTO_CONFIG", 'True'),
    "SET_BOT_CMD": os.getenv("SET_BOT_CMD", 'True'),
    "BOT_DESCRIPTION": os.getenv("BOT_DESCRIPTION", 'Welcome to Contactgram Bot! Super easily contact owners and admins!'),
    "BOT_SHORT_DESCRIPTION": os.getenv("BOT_SHORT_DESCRIPTION", 'Welcome to Contactgram Bot!'),
    "ENABLE_DETAILED_FORWARD": os.getenv("ENABLE_DETAILED_FORWARD") if os.getenv("ENABLE_DETAILED_FORWARD") else "True",
    "WELCOME_MESSAGE": os.getenv("WELCOME_MESSAGE", "Reply to this bot to contact the owner!"),
    "WELCOME_IMAGE_URL": os.getenv("WELCOME_IMAGE_URL") if os.getenv("WELCOME_IMAGE_URL") else "No Image",
}

def check_env():
    for key, value in env_dict.items():
        value = value.strip() if isinstance(value, str) else value
        if value in (None, ''):
            logger.error(f"Missing value for {key} in settings.env file")
            sys.exit(1)
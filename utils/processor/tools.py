import requests
from loguru import logger
from utils.processor.load_env import env_dict


def set_bot_info(info_type, info_value):
    url_map = {
        'name': f"https://api.telegram.org/bot{env_dict.get('BOT_TOKEN')}/setMyName",
        'description': f"https://api.telegram.org/bot{env_dict.get('BOT_TOKEN')}/setMyDescription",
        'short_description': f"https://api.telegram.org/bot{env_dict.get('BOT_TOKEN')}/setMyShortDescription",
        'commands': f"https://api.telegram.org/bot{env_dict.get('BOT_TOKEN')}/setMyCommands"
    }

    if info_type not in url_map:
        logger.error(
            f"Invalid info type '{info_type}'. Valid options are 'name', 'description', or 'short_description'.")
        return

    url = url_map[info_type]
    params = {info_type: info_value}

    response = requests.post(url, json=params)

    if response.status_code == 200:
        logger.info(f"Bot {info_type.replace('_', ' ').capitalize()} changed successfully.")
    else:
        logger.error(f"Failed to change bot {info_type.replace('_', ' ')}.")
        logger.error(response.text)

def get_file_id_and_text(update):
    if update.message.document:
        file_id = update.message.document.file_id
    elif update.message.photo:
        file_id = update.message.photo[-1].file_id
    elif update.message.video:
        file_id = update.message.video.file_id
    elif update.message.audio:
        file_id = update.message.audio.file_id
    elif update.message.sticker:
        file_id = update.message.sticker.file_id
    else:
        file_id = None

    if update.message.text:
        message_text = update.message.text
    elif update.message.caption:
        message_text = update.message.caption
    else:
        message_text = ''

    return file_id, message_text

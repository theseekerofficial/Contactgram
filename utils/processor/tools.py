import aiohttp
import requests
from loguru import logger
from datetime import datetime, timezone
from utils.processor.load_env import env_dict
from utils.database.db_initialize import chat_storage, db
from utils.processor.data_holders import admin_data, user_data, user_context_data


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

async def store_chat_message(context, user_id, message_id, message, msg_type, is_admin=False, admin_id=None, is_media=False,
                             is_forwarded=False, is_reply=False, reply_msg_id=None):
    if user_id not in user_data:
        user_data_obj = await context.bot.get_chat_member(chat_id=int(user_id), user_id=int(user_id))
        user_data[user_id] = user_data_obj

    if str(user_id) not in user_context_data:
        url = f"{env_dict.get('WEB_APP_URL')}/update-contact"
        payload = {
            "pass_access": env_dict.get("INTERFACE_PROCESS_PASSWORD"),
            "user_name": user_data[user_id].user.full_name if user_data[user_id].user.full_name else user_data[user_id].user.first_name if user_data[user_id].user.first_name else "Unknown User",
            "user_id": str(user_id)
        }

        async with aiohttp.ClientSession() as aio_session:
            async with aio_session.post(url, json=payload) as response:
                response_data = await response.json()
                if response_data.get("success") == "True":
                    logger.info(f"User contact data stored successfully.")
                else:
                    logger.error(f"Failed to store user contact data.")
                    logger.error(response_data)

        user_context_data.append(str(user_id))

    message_collection = chat_storage[str(user_id)]

    doc = {
            "message_id": message_id,
            "username": user_data[user_id].user.username if user_data[user_id].user.username else "N/A",
            "user_name": user_data[user_id].user.full_name if user_data[user_id].user.full_name else user_data[user_id].user.first_name if user_data[user_id].user.first_name else "Unknown User",
            "message": message,
            "is_admin": is_admin,
            "replied_admin_id": admin_id,
            "replied_admin_name": admin_data[str(admin_id)]["full_name"] if admin_id and str(admin_id) in admin_data else None,
            "timestamp": datetime.now(tz=timezone.utc),
            "msg_type": msg_type,
         }

    if is_forwarded:
        doc["is_forwarded"] = True
    if is_media:
        doc["is_media"] = True
    if is_reply and reply_msg_id:
        doc["is_reply"] = True
        doc["reply_msg_id"] = reply_msg_id

    await message_collection.insert_one(doc)

async def create_ttl_index():
    collections_with_ttl_indexes = [
        {"collection": db.Config, "field": "delete_at"}
    ]

    for item in collections_with_ttl_indexes:
        collection = item["collection"]
        field = item["field"]

        indexes = await collection.index_information()
        ttl_index_exists = any(field in index["key"][0] for index in indexes.values())

        if not ttl_index_exists:
            await collection.create_index([(field, 1)], expireAfterSeconds=0)
            logger.info(f"TTL index created for {collection.name} collection on '{field}'.")
        else:
            logger.info(f"TTL index already exists for {collection.name} on '{field}'.")
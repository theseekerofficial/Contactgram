import random
import asyncio
from loguru import logger
from telegram.ext import ContextTypes
from telegram import ReactionTypeEmoji
from utils.processor.load_env import env_dict
from utils.processor.tools import store_chat_message
from utils.database.db_initialize import chat_storage
from utils.processor.data_holders import admin_data, user_contact_data

admin_chat_ids = env_dict.get("ADMIN_TEAM")

ADMIN_TO_USER_REACTIONS = ["🏆", "👌", "💯", "🎉", "🚀"]

async def broadcast_admin_message(update, context, message, file_id, user_id, reply_to_message_id, is_forwarded=False):
    is_media = False
    if update.message.text:
        await context.bot.send_message(chat_id=user_id, text=message, parse_mode="html", reply_to_message_id=reply_to_message_id)
    elif update.message.photo:
        await context.bot.send_photo(chat_id=user_id, photo=file_id, caption=message, parse_mode="html", reply_to_message_id=reply_to_message_id)
        is_media = True
    elif update.message.video:
        await context.bot.send_video(chat_id=user_id, video=file_id, caption=message, parse_mode="html", reply_to_message_id=reply_to_message_id)
        is_media = True
    elif update.message.audio:
        await context.bot.send_audio(chat_id=user_id, audio=file_id, caption=message, parse_mode="html", reply_to_message_id=reply_to_message_id)
        is_media = True
    elif update.message.document:
        await context.bot.send_document(chat_id=user_id, document=file_id, caption=message, parse_mode="html", reply_to_message_id=reply_to_message_id)
        is_media = True
    elif update.message.sticker:
        await context.bot.forward_message(chat_id=user_id, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        is_media = True

    if not is_forwarded:
        try:
            random_emoji = random.choice(ADMIN_TO_USER_REACTIONS)
            await context.bot.set_message_reaction(
                chat_id=update.message.chat_id,
                message_id=update.message.message_id,
                reaction=[ReactionTypeEmoji(emoji=random_emoji)]
            )
        except Exception as e:
            logger.error(f"Error adding reaction to admin message: {str(e)}")

    if str(user_id) not in admin_chat_ids and env_dict.get("START_WEB_APP"):
        asyncio.create_task(store_chat_message(context, user_id,
                                               update.message.message_id,
                                               update.message.text if update.message.text else (update.message.caption if update.message.caption else '<code>No text content</code>'),
                                               'text', is_admin=True, admin_id=update.message.from_user.id, is_media=is_media,
                                               is_reply=True if reply_to_message_id else False, reply_msg_id=reply_to_message_id))

        logger.info(f"Admin reply forwarded to user {user_id}.")
    else:
        logger.info(f"Message Resent to admin successfully.")


async def load_admin_names(context: ContextTypes.DEFAULT_TYPE):
    admin_list = env_dict.get("ADMIN_TEAM")

    for admin_id in admin_list:
        admin_data[str(admin_id)] = {}
        try:
            user_info = await context.bot.get_chat_member(chat_id=int(admin_id), user_id=int(admin_id))
            if user_info.user.username:
                username = user_info.user.username if user_info.user.username else "N/A"
                full_name = user_info.user.full_name if user_info.user.full_name else user_info.user.first_name if user_info.user.first_name else "Unknown Admin"

                admin_data[str(admin_id)] = {
                    "username": username,
                    "full_name": full_name
                }
        except Exception as e:
            logger.error(f"Error loading admin username: {str(e)}")

async def load_user_contacts():
    if env_dict.get("START_WEB_APP"):
        logger.info("Loading user contacts...")
        collections = await chat_storage.list_collection_names()
        for collection_name in collections:
            collection = chat_storage[collection_name]
            doc = await collection.find_one({"user_name": {"$exists": True}}, {"user_name": 1, "_id": 0})
            if doc:
                user_contact_data[collection_name] = {}
                user_contact_data[collection_name]["user_name"] = doc["user_name"]
                user_contact_data[collection_name]["user_id"] = collection_name
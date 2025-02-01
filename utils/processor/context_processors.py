from loguru import logger
from utils.processor.load_env import env_dict

admin_chat_ids = env_dict.get("ADMIN_TEAM")


async def broadcast_admin_message(update, context, message, file_id, user_id, reply_to_message_id):
    if update.message.text:
        await context.bot.send_message(chat_id=user_id, text=message, parse_mode="html", reply_to_message_id=reply_to_message_id)
    elif update.message.photo:
        await context.bot.send_photo(chat_id=user_id, photo=file_id, caption=message, parse_mode="html", reply_to_message_id=reply_to_message_id)
    elif update.message.video:
        await context.bot.send_video(chat_id=user_id, video=file_id, caption=message, parse_mode="html", reply_to_message_id=reply_to_message_id)
    elif update.message.audio:
        await context.bot.send_audio(chat_id=user_id, audio=file_id, caption=message, parse_mode="html", reply_to_message_id=reply_to_message_id)
    elif update.message.document:
        await context.bot.send_document(chat_id=user_id, document=file_id, caption=message, parse_mode="html", reply_to_message_id=reply_to_message_id)
    elif update.message.sticker:
        await context.bot.forward_message(chat_id=user_id, from_chat_id=update.message.chat_id, message_id=update.message.message_id)

    if str(user_id) not in admin_chat_ids:
        logger.info(f"Admin reply forwarded to user {user_id}.")
    else:
        logger.info(f"Message Resent to admin successfully.")

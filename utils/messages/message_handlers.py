import re
from loguru import logger
from telegram.ext import CallbackContext
from utils.processor.load_env import env_dict
from utils.processor.context_processors import broadcast_admin_message
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from utils.processor.tools import get_file_id_and_text

admin_chat_ids = env_dict.get("ADMIN_TEAM")


async def forward_to_admin(update: Update, context: CallbackContext):
    try:
        user_id = update.message.from_user.id
        if context.user_data.get("forward_mode_target", None):
            return
        if str(user_id) in str(env_dict.get("BOT_ID")):
            return
        if str(user_id) in admin_chat_ids and not update.message.reply_to_message:
            await update.message.reply_text("Reply to a user's message in order to reply directly to them. If you want to forward somthing to user, use /forwardmode cmd", reply_to_message_id=update.message.message_id)
            return
        elif str(user_id) in admin_chat_ids and update.message.reply_to_message:
            return

        username = update.message.from_user.username if update.message.from_user.username else "N/A"
        user_mention = update.message.from_user.mention_html() if update.message.from_user else "N/A"

        formatted_message = f"#{username}\n\n{update.message.text if update.message.text else (update.message.caption if update.message.caption else '<code>No text content</code>')}\n\n<code>[</code> <code>{user_id}</code> | @{username} | {user_mention} | {update.message.message_id} <code>]</code>"

        if len(formatted_message) > 1024 and (update.message.video or update.message.document or update.message.sticker or update.message.photo or update.message.audio):
            await update.message.reply_text("Caption is too long. Please try again with a shorter message.", reply_to_message_id=update.message.message_id)
            return
        if len(formatted_message) > 4096 and update.message.text:
            await update.message.reply_text("Message is too long. Please try again with a shorter message.", reply_to_message_id=update.message.message_id)
            return

        keyboard = [
            [InlineKeyboardButton("Mark as Seen 👀", callback_data=f"seen_{user_id}_{update.message.message_id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        for admin_chat_id in admin_chat_ids:
            if env_dict.get("ENABLE_DETAILED_FORWARD").capitalize() == "True":
                try:
                    if update.message.text:
                        await context.bot.send_message(chat_id=admin_chat_id.strip(), text=formatted_message,
                                                       parse_mode="html", reply_markup=reply_markup)
                    elif update.message.photo:
                        await context.bot.send_photo(chat_id=admin_chat_id.strip(),
                                                     photo=update.message.photo[-1].file_id,
                                                     caption=formatted_message, parse_mode="html",
                                                     reply_markup=reply_markup)
                    elif update.message.video:
                        await context.bot.send_video(chat_id=admin_chat_id.strip(), video=update.message.video.file_id,
                                                     caption=formatted_message, parse_mode="html",
                                                     reply_markup=reply_markup)
                    elif update.message.audio:
                        await context.bot.send_audio(chat_id=admin_chat_id.strip(), audio=update.message.audio.file_id,
                                                     caption=formatted_message, parse_mode="html",
                                                     reply_markup=reply_markup)
                    elif update.message.document:
                        await context.bot.send_document(chat_id=admin_chat_id.strip(),
                                                        document=update.message.document.file_id,
                                                        caption=formatted_message,
                                                        parse_mode="html", reply_markup=reply_markup)
                    elif update.message.sticker:
                        sticker_message = await context.bot.forward_message(chat_id=admin_chat_id.strip(),
                                                                            from_chat_id=user_id,
                                                                            message_id=update.message.message_id)
                        await context.bot.send_message(chat_id=admin_chat_id.strip(), text=formatted_message,
                                                       parse_mode="html",
                                                       reply_to_message_id=sticker_message.message_id,
                                                       reply_markup=reply_markup)
                    else:
                        await update.message.reply_text("Your message contains unsupported content that I cannot process. If this issue persists, please inform the bot owner.",
                                                        reply_to_message_id=update.message.message_id)
                        return
                except Exception as e:
                    logger.error(f"Error forwarding message: {str(e)}")
                    await context.bot.send_message(chat_id=admin_chat_id.strip(),
                                                   text=f"Error forwarding message: {str(e)}", parse_mode="html")
                    continue
            else:
                forwarded_message = await context.bot.forward_message(chat_id=admin_chat_id.strip(), from_chat_id=user_id,
                                                  message_id=update.message.message_id)

                metadata = f"#{username}\n\n<i>User ID: </i><code>{user_id}</code>\n<i>Username: </i>@{username}\n<i>User Link: </i>{user_mention}\n<i>MSG ID: {update.message.message_id}</i>"
                await context.bot.send_message(chat_id=admin_chat_id.strip(), text=metadata, parse_mode="html", reply_to_message_id=forwarded_message.message_id)

        logger.info(f"Message from {update.message.chat.username} forwarded to Admin Team.")
    except Exception as e:
        logger.error(f"Error forwarding message: {str(e)}")


async def handle_admin_reply(update: Update, context: CallbackContext):
    try:
        file_id, message_text = get_file_id_and_text(update)
        # Detailed Text Mode
        if not update.message.reply_to_message.forward_origin and update.message.reply_to_message.from_user.id == env_dict.get("BOT_ID") and str(update.message.from_user.id) in admin_chat_ids and update.message.reply_to_message.text:
            reply_message = update.message.reply_to_message.text
            user_id_str = reply_message.split("[")[-1].split("]")[0]
            user_id = int(user_id_str.split("|")[0].strip())

            if context.user_data.get("reply_enabled", False):
                msg_id = int(user_id_str.split("|")[3].strip())
            else:
                msg_id = None

            await broadcast_admin_message(update, context, f"{message_text}", file_id, user_id, msg_id)

        # Detailed Caption Mode
        elif not update.message.reply_to_message.forward_origin and update.message.reply_to_message.from_user.id == env_dict.get("BOT_ID") and str(update.message.from_user.id) in admin_chat_ids and update.message.reply_to_message.caption:
            reply_message = update.message.reply_to_message.caption
            user_id_str = reply_message.split("[")[-1].split("]")[0]
            user_id = int(user_id_str.split("|")[0].strip())

            if context.user_data.get("reply_enabled", False):
                msg_id = int(user_id_str.split("|")[3].strip())
            else:
                msg_id = None

            await broadcast_admin_message(update, context, f"{message_text}", file_id, user_id, msg_id)

        # Forwarded Mode
        elif update.message.reply_to_message.forward_origin and str(update.message.from_user.id) in admin_chat_ids and update.message.text:
            user_id = update.message.reply_to_message.forward_origin.sender_user.id
            if env_dict.get("ENABLE_DETAILED_FORWARD").capitalize() != "True":
                if "id:" in message_text and re.search(r'id:\d+', message_text):
                    msg_id = message_text.split("id:")[-1].strip()
                    message_text = re.sub(r'id:\d+$', '', message_text)
                else:
                    msg_id = None
            else:
                msg_id = None

            await broadcast_admin_message(update, context, f"{message_text}", file_id, user_id, msg_id)

    except Exception as e:
        logger.error(f"Error handling admin reply: {str(e)}")


async def handle_admin_forwards(update: Update, context: CallbackContext):
    if context.user_data.get("forward_mode_target", None):
        file_id, message_text = get_file_id_and_text(update)
        user_id = context.user_data.get("forward_mode_target")
        message_id = update.message.message_id
        if len(message_text) > 1024:
            message_text = message_text[:1000] + "..."
        message_text += "\n\n<code>Forwarded ✅</code>"

        await context.bot.forward_message(chat_id=user_id, from_chat_id=update.message.chat_id, message_id=message_id)
        await update.message.delete()
        await broadcast_admin_message(update, context, message_text, file_id, update.message.from_user.id, None)

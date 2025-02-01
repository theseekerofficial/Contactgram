from loguru import logger
from telegram.ext import CallbackContext

from utils.commands.command_handlers import send_help_page
from utils.database.db_initialize import db
from utils.processor.load_env import env_dict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

admin_chat_ids = env_dict.get("ADMIN_TEAM")


async def handle_mark_as_seen(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        callback_data = query.data

        _, user_id, message_id = callback_data.split("_")

        if len(admin_chat_ids) > 1:
            previous_data_doc = await db.Seen_Messages.find_one({"user_id": int(user_id)})
            if previous_data_doc:
                for item in previous_data_doc["seen_messages"]:
                    if item['message_id'] == int(message_id):
                        admin_user = await context.bot.get_chat_member(int(item['admin_id']), int(item['admin_id']))
                        admin_name = admin_user.user.full_name if admin_user else "Unknown Admin"
                        await query.answer(text=f"This message has already been marked as seen by {admin_name} admin.", show_alert=True)
                        return

        admin_user = await context.bot.get_chat_member(query.from_user.id, query.from_user.id)
        admin_name = admin_user.user.full_name if admin_user else "Unknown Admin"

        await context.bot.send_message(chat_id=user_id, text=f"{admin_name} <i>saw your message. Wait for a reply...</i>",
                                       parse_mode="html", reply_to_message_id=int(message_id), disable_notification=True)

        await db.Seen_Messages.update_one(
            {"user_id": int(user_id)},
            {"$push": {"seen_messages": {'message_id': int(message_id), 'admin_id': int(query.from_user.id)}}},
            upsert=True
        )

        user_obj = await context.bot.get_chat_member(user_id, int(user_id))
        await query.answer(text=f"Informed {user_obj.user.full_name if user_obj else 'Unknown User'} to that you saw their message.")
        new_keyboard = [
            [InlineKeyboardButton("Marked as Seen 🔖", callback_data="already_seen")]
        ]
        new_reply_markup = InlineKeyboardMarkup(new_keyboard)
        await query.edit_message_reply_markup(reply_markup=new_reply_markup)

        logger.info(f"User {user_id}'s message {message_id} marked as seen by {admin_name} admin.")

        await query.answer()

    except Exception as e:
        logger.error(f"Error handling callback: {str(e)}")

async def handle_already_seen(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        await query.answer(text="This message has already been marked as seen.", show_alert=True)
    except Exception as e:
        logger.error(f"Error handling 'already_seen' callback: {str(e)}")

async def handle_help_navigation(update, context):
    query = update.callback_query
    callback_data = query.data
    page_number = None

    if callback_data.startswith("help_next"):
        page_number = int(callback_data.split("_")[2])
    elif callback_data.startswith("help_previous"):
        page_number = int(callback_data.split("_")[2])

    if page_number is not None:
        await send_help_page(update, page_number)

    await query.answer()
import telegram
from loguru import logger
from datetime import datetime, timezone
from telegram.ext import CallbackContext
from utils.processor.load_env import env_dict
from utils.database.db_initialize import user_collection
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

admin_chat_ids = env_dict.get("ADMIN_TEAM")

HELP_PAGES = [
    {
        "page": 1,
        "text": """<b>Welcome to <u>Contactgram</u> - Your Telegram Contact Management Bot 🤖</b>

<i><u>Contactgram</u> is designed to help admins efficiently manage and communicate with a large number of users without flooding their inboxes. It's incredibly easy to use and helps you keep your interactions smooth and organized! 💬</i>

<b><u>Basic Commands:</u></b> 📝

- <code>/start</code>: <i>Start the bot and initialize the interaction. 🚀</i>

- <code>/help</code>: <i>Get detailed help and instructions on how to use the bot. 🆘</i>

- <code>/togglereply</code>: <i>Toggle between sending normal messages and sending replies to the user's messages. <b>[Only for admin team]</b> 🛡️</i>

- <code>/forwardmode</code>: <i>Instead of sending messages directly to users, forward messages when an admin forwards a message to the bot. <b>Usage: <code>/forwardmode &lt;user tg id&gt;</code> Example: <code>/forwardmode 123456789</code>. Admins can activate this mode using the reply to a user message. 🔄</b></i> <b>[Only for admin team]</b>

Click "<b>Next</b>" to see more features! 👇
""",
        "buttons": [
            [InlineKeyboardButton("⫸ Next ⫸", callback_data="help_next_2")]
        ]
    },
    {
        "page": 2,
        "text": """<b><u>Features</u> ✨</b>

- <i><b>Mark as Seen</b></i>: Admins can notify users that their message has been seen, allowing them to wait for a reply. 👀

- <i><b>Instant Messages</b></i>: Messages are transferred instantly between admins and users, ensuring smooth and fast communication. ⚡

- <i><b>Message Modes in Contactgram</b></i>: 
  - <i><code>/togglereply</code></i>: Toggle reply mode to send replies to specific user messages. 🔄
  - <i><code>/forwardmode</code></i>: Admins can use this mode to forward messages to users instead of sending them directly. Usage: <i><code>/forwardmode &lt;tg_user_id&gt;</code></i> or reply to a user's message with the <i><code>/forwardmode</code></i> command. 📨

- <i><b>Multi-Admin Support</b></i>: The bot supports multiple admins, making it easy to manage a team and delegate tasks. 👥

Click "<b>Previous</b>" to go back or "<b>Next</b>" to continue. 🔁
""",
        "buttons": [
            [InlineKeyboardButton("⫷ Previous ⫷", callback_data="help_previous_1"),
             InlineKeyboardButton("⫸ Next ⫸", callback_data="help_next_3")]
        ]
    },
    {
        "page": 3,
        "text": """<b><u>Additional Info</u> 🔎</b>

This bot is packed with multiple features to enhance the user experience:
- Admin controls and settings ⚙️
- Customizable commands and welcome messages ✨
- Seamless interaction between admins and users 👫

<b><u>Creator Credits:</u> 👑</b>
- Created by: <i><b>The Seeker</b></i> 🕵️‍♂️
- Update Channel: <a href="https://t.me/Maste_Torrenz_Updates"><u>Master Torrenz Updates</u></a> 📢
- Contact The Seeker via Contactgram: <a href="https://t.me/The_Seeker_Contact_Robot"><u>@The_Seeker_Contact_Robot</u></a> 💬
- Email: <a href="mailto:caveoftheseekers@gmail.com"><u>caveoftheseekers@gmail.com</u></a> 📧

<b><u>Other Services by The Seeker:</u> 💻</b>
- <b><i>MLWA (Mirror Leech Web App)</i></b>: <a href="https://mlwa.xyz"><u>mlwa.xyz</u></a> 🌐
  - Update Channel: <a href="https://t.me/Mirror_Leech_Web_App"><u>Mirror Leech Web App</u></a> 🔄

- <b><i>Echo</i></b> (A Multi-Functional Ultra User Assistant): <a href="https://github.com/theseekerofficial/Echo"><u>Echo on GitHub</u></a> 🖥️
  - Update Channel: <a href="https://t.me/Echo_AIO"><u>Echo AIO</u></a> 🆙

Thank you for using the bot! Feel free to contact us for support. 🤝

Click "<b>Previous</b>" to go back to the previous page. 🔙
""",
        "buttons": [
            [InlineKeyboardButton("⫷ Previous ⫷", callback_data="help_previous_2")],
            [InlineKeyboardButton("Contactgram Repo ⚙️", url="https://github.com/theseekerofficial/Contactgram")]
        ]
    }
]

async def start(update: Update, context: CallbackContext):
    try:
        user_id = update.message.from_user.id
        existing_user = await user_collection.find_one({"telegram_id": int(user_id)})

        if not existing_user and str(user_id) not in admin_chat_ids:
            user_data = {
                "name": update.message.from_user.first_name,
                "username": update.message.from_user.username if update.message.from_user.username else "N/A",
                "telegram_id": user_id,
                "start_time": datetime.now(tz=timezone.utc)
            }

            await user_collection.insert_one(user_data)
            logger.info(f"User {update.message.from_user.username} data stored in MongoDB.")

            for admin_chat_id in admin_chat_ids:
                sent_photo = await context.bot.send_photo(admin_chat_id.strip(),
                                                          'assets/user.jpg',
                                                          caption=f"#New_User started {env_dict.get('BOT_NAME')}\n\n<b><u><i>User Info:</i></u></b>\n\nName: <code>{user_data['name']}</code>\nUsername: @{user_data['username']}\nTelegram ID: <code>{user_data['telegram_id']}</code>\nStart Time: <code>{user_data['start_time']}</code>\n\nUser link: {update.message.from_user.mention_html() if update.message.from_user else 'N/A'}",
                                                          parse_mode="html")
                await sent_photo.pin(disable_notification=False)

        if not str(user_id) in admin_chat_ids:
            welcome_message = f"<b>Welcome to {env_dict.get('BOT_NAME')}!</b>\n\n{env_dict.get('WELCOME_MESSAGE')}\n\n<i>Developed by The Seeker. Create your own contactgram bot using official repo</i>"

            keyboard = [
                [InlineKeyboardButton("Contactgram Repo 🛠️", url="https://github.com/theseekerofficial/Contactgram")],
                [InlineKeyboardButton("Update Channel 📢", url="https://t.me/Maste_Torrenz_Updates")]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
        else:
            welcome_message = f"Your {env_dict.get('BOT_NAME')} alive and listening to all your users"
            reply_markup = None

        if env_dict.get("WELCOME_IMAGE_URL").startswith("http"):
            await context.bot.send_photo(chat_id=user_id, photo=env_dict.get("WELCOME_IMAGE_URL"), caption=welcome_message,
                                         parse_mode="html", reply_markup=reply_markup)
        else:
            await context.bot.send_message(chat_id=user_id, text=welcome_message, parse_mode="html", reply_markup=reply_markup)

        logger.info(
            f"Welcome message sent to user {update.message.from_user.username} after starting the bot."
        )
    except Exception as e:
        logger.error(f"Error storing user data: {str(e)}")

async def help_load(update, context):
    await send_help_page(update, page_number=1, start_page=True)

async def toggle_reply(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if str(user_id) not in admin_chat_ids:
        await update.message.reply_text("Sorry champ. This command only for admins!", reply_to_message_id=update.message.message_id)
        return

    if env_dict.get("ENABLE_DETAILED_FORWARD").capitalize() != "True":
        await update.message.reply_text("Reply mode change not available when <code>'ENABLE_DETAILED_FORWARD'</code> is disabled. Please set <code>'ENABLE_DETAILED_FORWARD'</code> ENV in settings.env to <code>True</code> to enable this feature.\n\n"
                                        "To reply to a specific message when 'ENABLE_DETAILED_FORWARD' disabled, use the id: tag followed by the message ID (e.g., id:213) <u>at the end of your message</u>. This lets the bot reply directly to that message in the chat. Full example:\n\n<code>Hey, this is an admin message. id:213</code>"
                                        "\n\nThis will allow the bot to respond directly to the 213th message in that chat.",
                                        reply_to_message_id=update.message.message_id, parse_mode="html")
        return

    current_value = context.user_data.get("reply_enabled", False)
    new_value = not current_value

    context.user_data["reply_enabled"] = new_value

    logger.info(f"Reply mode changed to {new_value} for user {update.message.from_user.full_name if update.message.from_user else 'N/A'} admin.")

    if new_value:
        await update.message.reply_text("Reply mode have been <code>enabled</code>. Now your messages sent as replies to user's original messages",
                                        parse_mode="html", reply_to_message_id=update.message.message_id)
    else:
        await update.message.reply_text("Reply mode have been <code>disabled</code>. Now your messages send as normal messages",
                                        parse_mode="html", reply_to_message_id=update.message.message_id)

async def handle_forward_mode(update: Update, context: CallbackContext):
    interact_user_id = update.message.from_user.id
    if str(interact_user_id) not in admin_chat_ids:
        await update.message.reply_text("Sorry champ. This command only for admins!", reply_to_message_id=update.message.message_id)
        return

    if context.user_data.get("forward_mode_target", None):
        context.user_data.pop("forward_mode_target", None)
        await update.message.reply_text("Forward mode turned off successfully. Now your messages will be sent as normal messages.",)
        return

    if update.message.reply_to_message:
        if update.message.reply_to_message.forward_origin:
            user_id = update.message.reply_to_message.forward_origin.sender_user.id
            context.user_data["forward_mode_target"] = user_id
        else:
            await update.message.reply_text("Reply to forwarded message of a user or sent user id along with cmd. Example: /forwardmode 1234567890", reply_to_message_id=update.message.message_id)
            return
    else:
        user_id = ' '.join(context.args)
        if not user_id:
            await update.message.reply_text("Please provide a valid Telegram ID to forward messages to. Or reply to user's message with /forwardmode cmd.",
                                            reply_to_message_id=update.message.message_id)
            return

        if user_id.isdigit():
            context.user_data["forward_mode_target"] = user_id
        else:
            await update.message.reply_text("Invalid Telegram ID. Please provide a valid Telegram ID or Username to forward messages to. Or reply to user's message with /forwardmode cmd.",)
            return
    try:
        user_name_obj = await context.bot.get_chat(user_id)
        user_name = user_name_obj.full_name if user_name_obj else "Unknown User"
    except telegram.error.BadRequest as e:
        logger.error(f"Error getting user name: {str(e)}")
        await update.message.reply_text(f"Invalid Telegram ID. Please provide a valid Telegram ID or Username to forward messages to. Or reply to user's message with /forwardmode cmd.",
                                        reply_to_message_id=update.message.message_id)
        context.user_data.pop("forward_mode_target", None)
        return

    await update.message.reply_text(f"Forward mode target set to <code>{user_name}</code>. Now forward anything to me and I ll deliver it to <code>{user_name}</code>.\n\nWhenever you want to stop forwarding, simply send /forwardmode again",
                                    reply_to_message_id=update.message.message_id, parse_mode="html")

async def send_help_page(update, page_number, start_page=False):
    help_page = HELP_PAGES[page_number - 1]
    message = help_page["text"]
    buttons = help_page["buttons"]

    if start_page:
        await update.message.reply_text(
            message,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="html",
            reply_to_message_id=update.message.message_id
        )
        return

    await update.callback_query.message.edit_text(
        message,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="html"
    )
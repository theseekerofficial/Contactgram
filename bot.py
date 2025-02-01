# bot.py
# Developed by The Seeker [https://t.me/The_Seeker_Contact_Robot]

from loguru import logger
from logger_config import configure_logger
from utils.processor.tools import set_bot_info
from utils.processor.load_env import env_dict, check_env
from utils.commands.command_handlers import start, toggle_reply, handle_forward_mode, help_load
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from utils.messages.message_handlers import forward_to_admin, handle_admin_reply, handle_admin_forwards
from utils.callbacks.callback_handlers import handle_mark_as_seen, handle_already_seen, handle_help_navigation


bot_token = env_dict.get("BOT_TOKEN")

bot_commands = [
    {
        "command": "start",
        "description": f"Start the {env_dict.get('BOT_NAME')} 🔗"
    },
    {
        "command": "help",
        "description": "Get help & more info message 💁"
    },
    {
        "command": "togglereply",
        "description": "Toggle send messages as replies or not to users (Only Admin) 🛡️"
    },
    {
        "command": "forwardmode",
        "description": "Toggle forward messages to specific user or not (Only Admin) 🛡️"
    }
]


def main():
    logger.info("Starting Contactgram Bot...")
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler('help', help_load))
    application.add_handler(CommandHandler('togglereply', toggle_reply))
    application.add_handler(CommandHandler('forwardmode', handle_forward_mode))

    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, forward_to_admin), group=1)
    application.add_handler(MessageHandler(filters.REPLY & ~filters.COMMAND, handle_admin_reply), group=2)
    application.add_handler(MessageHandler(filters.FORWARDED & ~filters.COMMAND, handle_admin_forwards), group=3)

    application.add_handler(CallbackQueryHandler(handle_mark_as_seen, pattern=r"^seen_.*$"))
    application.add_handler(CallbackQueryHandler(handle_already_seen, pattern=r"^already_seen$"))
    application.add_handler(CallbackQueryHandler(handle_help_navigation, pattern=r"^help_(next|previous)_\d+$"))

    if env_dict.get("AUTO_CONFIG").capitalize() == "True":
        if env_dict.get("SET_BOT_CMD", "True").capitalize() == "True":
            set_bot_info('commands', bot_commands)

        set_bot_info('name', env_dict.get("BOT_NAME"))
        set_bot_info('description', env_dict.get("BOT_DESCRIPTION"))
        set_bot_info('short_description', env_dict.get("BOT_SHORT_DESCRIPTION"))

    return application

if __name__ == "__main__":
    configure_logger()
    check_env()

    app = main()
    if env_dict.get("ENABLE_DETAILED_FORWARD").capitalize() != "True":
        logger.warning("Detailed Forward Mode is disabled. This mode as less capabilities compared to the detailed mode. "
                       "For more admin and user experience it's highly recommended to use detailed mode.")
    logger.info(f"PRODUCT OF TSSC | Creator: ꓄ꃅꍟ ꌗꍟꍟꀘꍟꋪ [https://t.me/MrUnknown411]")
    app.run_polling()
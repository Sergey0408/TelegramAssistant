import logging
import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from bot_handlers import start, help_command, multiply, button_handler, handle_number_input
from user_state import UserState

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def main():
    """Start the bot."""
    # Create the Application
    token = "7606023414:AAE28ed3M7FRBz_kV0fwbN-gsdAef0Xfw4U"
    application = ApplicationBuilder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("multiply", multiply))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number_input))

    # Start the Bot using run_polling() method
    application.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == '__main__':
    main()
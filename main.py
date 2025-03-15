import logging
import os
import signal
import nest_asyncio
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
import asyncio
from threading import Thread

from bot_handlers import start, help_command, multiply, button_handler, handle_number_input
from user_state import UserState

# Create Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return 'Telegram Bot is running!'

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)
application = None

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info("Received shutdown signal, cleaning up...")
    if application:
        try:
            application.stop()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}", exc_info=True)
    logger.info("Cleanup complete")

async def run_bot():
    """Start the bot."""
    global application

    try:
        # Create the Application
        token = "7606023414:AAE28ed3M7FRBz_kV0fwbN-gsdAef0Xfw4U"
        logger.info("Initializing bot with token...")

        # Build application
        application = ApplicationBuilder().token(token).build()

        # First, delete any existing webhook
        logger.info("Removing existing webhook...")
        await application.bot.delete_webhook()

        # Add handlers
        logger.info("Registering command handlers...")
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("multiply", multiply))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number_input))

        # Error handler
        async def error_handler(update, context):
            """Log errors and send a message to the user."""
            logger.error(f"Update {update} caused error {context.error}")
            if hasattr(context.error, "__traceback__"):
                logger.error(context.error, exc_info=True)

            if update and update.effective_message:
                await update.effective_message.reply_text(
                    "Произошла ошибка. Пожалуйста, попробуйте еще раз или начните заново с команды /start"
                )

        application.add_error_handler(error_handler)

        # Start the Bot using run_polling() method
        logger.info("Starting bot polling...")
        await application.run_polling(allowed_updates=["message", "callback_query"])
    except Exception as e:
        logger.error(f"Failed to start bot: {e}", exc_info=True)
        raise

def start_bot():
    """Start the bot in a separate thread."""
    try:
        # Apply nest_asyncio to allow nested event loops
        nest_asyncio.apply()
        logger.info("Starting bot application...")
        asyncio.run(run_bot())
    except Exception as e:
        logger.error(f"Bot stopped due to error: {e}", exc_info=True)

# Register signal handlers in the main thread
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Start bot in a separate thread when not in reloader or gunicorn worker
if not os.environ.get('WERKZEUG_RUN_MAIN') and not os.environ.get('GUNICORN_WORKER'):
    bot_thread = Thread(target=start_bot)
    bot_thread.daemon = True
    bot_thread.start()

if __name__ == '__main__':
    # Run Flask without debug mode to avoid multiple bot instances
    app.run(host='0.0.0.0', port=5000, debug=False)
import logging
import os
import signal
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from bot_handlers import start, help_command, multiply, button_handler, handle_number_input
from user_state import UserState

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Changed to DEBUG for more detailed logs
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

async def main():
    """Start the bot."""
    global application

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Create the Application
        token = "7606023414:AAE28ed3M7FRBz_kV0fwbN-gsdAef0Xfw4U"
        logger.info("Initializing bot with token...")

        # Build application with clean start
        application = ApplicationBuilder().token(token).build()

        # First, delete any existing webhook
        logger.info("Removing existing webhook...")
        await application.bot.delete_webhook(drop_pending_updates=True)

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
        await application.initialize()
        await application.start()
        await application.run_polling(allowed_updates=["message", "callback_query"], drop_pending_updates=True)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}", exc_info=True)
        raise
    finally:
        logger.info("Bot shutdown initiated")
        if application:
            try:
                await application.stop()
            except Exception as e:
                logger.error(f"Error during shutdown: {e}", exc_info=True)
        logger.info("Bot shutdown complete")

if __name__ == '__main__':
    import asyncio
    try:
        logger.info("Starting bot application...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot stopped due to error: {e}", exc_info=True)
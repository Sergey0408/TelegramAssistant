from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import time
import logging
from game_logic import GameLogic
from keyboard_utils import create_number_keyboard, create_difficulty_keyboard
from user_state import UserState
from sound_manager import play_sound

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user_id = update.effective_user.id
    logger.debug(f"Start command received from user {user_id}")
    logger.info(f"User {user_id} started the bot")

    welcome_message = (
        "👋 Привет! Я бот для изучения таблицы умножения.\n\n"
        "🎯 Используйте команду /multiply чтобы начать тренировку.\n"
        "❓ Используйте /help для получения справки."
    )
    logger.debug(f"Sending welcome message to user {user_id}")
    await update.message.reply_text(welcome_message)
    logger.info(f"Welcome message sent to user {user_id}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user_id = update.effective_user.id
    logger.debug(f"Help command received from user {user_id}")
    logger.info(f"User {user_id} requested help")

    help_text = (
        "📖 Как пользоваться ботом:\n\n"
        "1. Нажмите /multiply чтобы начать\n"
        "2. Выберите уровень сложности\n"
        "3. Решайте примеры, используя цифровую клавиатуру\n"
        "4. После 10 правильных ответов вы увидите свою статистику\n\n"
        "🎮 Удачи в обучении!"
    )
    logger.debug(f"Sending help text to user {user_id}")
    await update.message.reply_text(help_text)
    logger.info(f"Help text sent to user {user_id}")

async def multiply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start multiplication game."""
    user_id = update.effective_user.id
    logger.debug(f"Multiply command received from user {user_id}")
    logger.info(f"User {user_id} started multiplication game")

    keyboard = create_difficulty_keyboard()
    logger.debug(f"Created difficulty keyboard for user {user_id}")
    await update.message.reply_text(
        "Выберите уровень сложности:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    logger.info(f"Difficulty selection sent to user {user_id}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses."""
    query = update.callback_query
    await query.answer()  # Acknowledge the button press
    logger.info(f"User {query.from_user.id} pressed button with data: {query.data}")

    if query.data.startswith('level_'):
        level = query.data.split('_')[1]
        logger.debug(f"Starting new game with level: {level}")
        UserState.start_new_game(query.from_user.id, level)
        await show_next_question(query)
    elif query.data == 'continue':
        logger.debug("User pressed continue, showing next question")
        await show_next_question(query)
    elif query.data == 'new_game':
        logger.debug("User wants to start a new game, showing difficulty selection")
        keyboard = create_difficulty_keyboard()
        await query.edit_message_text(
            "Выберите уровень сложности:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data.isdigit():  # Handle numeric buttons
        # Add button click sound
        await play_sound("button")
        user_id = query.from_user.id
        game_state = UserState.get_user_state(user_id)
        logger.debug(f"User {user_id} pressed digit: {query.data}")

        if not game_state or not game_state.current_question:
            logger.warning(f"User {user_id} tried to answer without active game")
            await query.edit_message_text("Пожалуйста, начните игру с команды /multiply")
            return

        try:
            current_digit = query.data
            logger.debug(f"Processing digit input: {current_digit}")

            num1, num2 = game_state.current_question
            correct_answer = num1 * num2
            time_spent = int(time.time() - game_state.start_time)
            remaining_examples = 10 - game_state.correct_answers
            status_text = f"⏱ Время: {time_spent} сек\n📝 Осталось примеров: {remaining_examples}"

            # If this is the first digit
            if game_state.partial_answer is None:
                if correct_answer < 10:  # Single digit answer
                    user_answer = int(current_digit)
                    logger.debug(f"Processing single digit answer: {user_answer}")
                else:  # Start collecting digits for two-digit answer
                    game_state.partial_answer = current_digit
                    logger.debug(f"Started collecting digits: {game_state.partial_answer}")
                    keyboard = create_number_keyboard()
                    await query.edit_message_text(
                        f"{status_text}\n\nВведите вторую цифру ответа\n{num1} x {num2} = {current_digit}...",
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    )
                    return
            else:  # This is the second digit
                user_answer = int(game_state.partial_answer + current_digit)
                logger.debug(f"Completed two-digit answer: {user_answer}")
                game_state.partial_answer = None  # Reset for next question

            if user_answer == correct_answer:
                await play_sound("correct")
                game_state.correct_answers += 1
                remaining_examples = 10 - game_state.correct_answers
                keyboard = [[InlineKeyboardButton("Продолжить", callback_data='continue')]]
                await query.edit_message_text(
                    f"{status_text}\n\n✅ Правильно! Молодец!",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            else:
                await play_sound("wrong")
                game_state.errors += 1
                game_state.last_error = (num1, num2)
                keyboard = [[InlineKeyboardButton("Продолжить", callback_data='continue')]]
                await query.edit_message_text(
                    f"{status_text}\n\n❌ Ошибка!\nПравильный ответ: {num1} x {num2} = {correct_answer}",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )

        except ValueError as e:
            logger.error(f"Error processing answer for user {user_id}: {e}")
            await query.edit_message_text("Пожалуйста, введите число")

async def show_next_question(query):
    """Show the next question to the user."""
    user_id = query.from_user.id
    game_state = UserState.get_user_state(user_id)

    if not game_state:
        logger.warning(f"No game state found for user {user_id}")
        await query.edit_message_text(
            "Выберите уровень сложности:",
            reply_markup=InlineKeyboardMarkup(create_difficulty_keyboard())
        )
        return

    if game_state.correct_answers >= 10:
        time_taken = int(time.time() - game_state.start_time)
        logger.info(f"User {user_id} completed the game with {game_state.errors} errors in {time_taken} seconds")
        keyboard = [[InlineKeyboardButton("Начать новую игру", callback_data='new_game')]]
        await query.edit_message_text(
            f"🎉 Поздравляем! Вы завершили тренировку!\n"
            f"⏱ Затраченное время: {time_taken} секунд\n"
            f"❌ Количество ошибок: {game_state.errors}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        UserState.clear_user_state(user_id)
        return

    # Calculate current status
    time_spent = int(time.time() - game_state.start_time)
    remaining_examples = 10 - game_state.correct_answers
    status_text = f"⏱ Время: {time_spent} сек\n📝 Осталось примеров: {remaining_examples}"

    if game_state.last_error:
        # If there was an error in the previous question, ask it again
        num1, num2 = game_state.last_error
        game_state.current_question = (num1, num2)
        game_state.last_error = None  # Clear the error after setting it as current question
        logger.info(f"Repeating error question for user {user_id}: {num1} x {num2}")
        keyboard = create_number_keyboard()
        await query.edit_message_text(
            f"{status_text}\n\nДавай повторим сложный пример:\n{num1} x {num2}=",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # Generate new question
    num1, num2 = GameLogic.generate_numbers(game_state.level)
    game_state.current_question = (num1, num2)
    logger.info(f"Generated question for user {user_id}: {num1} x {num2}")

    keyboard = create_number_keyboard()
    await query.edit_message_text(
        f"{status_text}\n\nСколько будет {num1} x {num2}=",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
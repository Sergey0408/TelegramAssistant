from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_number_keyboard() -> list[list[InlineKeyboardButton]]:
    """Create numeric keyboard for answers with larger text."""
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="1"),
            InlineKeyboardButton("2", callback_data="2"),
            InlineKeyboardButton("3", callback_data="3"),
        ],
        [
            InlineKeyboardButton("4", callback_data="4"),
            InlineKeyboardButton("5", callback_data="5"),
            InlineKeyboardButton("6", callback_data="6"),
        ],
        [
            InlineKeyboardButton("7", callback_data="7"),
            InlineKeyboardButton("8", callback_data="8"),
            InlineKeyboardButton("9", callback_data="9"),
        ],
        [InlineKeyboardButton("0", callback_data="0")],
    ]
    return keyboard

def create_difficulty_keyboard() -> list[list[InlineKeyboardButton]]:
    """Create keyboard for difficulty selection with larger text."""
    keyboard = [
        [InlineKeyboardButton("x1-3 Легкий уровень", callback_data="level_easy")],
        [InlineKeyboardButton("x3-6 Средний уровень", callback_data="level_medium")],
        [InlineKeyboardButton("x6-9 Сложный уровень", callback_data="level_hard")],
        [InlineKeyboardButton("x1-9 Полный диапазон", callback_data="level_full")],
    ]
    return keyboard
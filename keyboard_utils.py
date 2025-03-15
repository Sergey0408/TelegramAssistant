from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_number_keyboard() -> list[list[InlineKeyboardButton]]:
    """Create numeric keyboard for answers with larger text."""
    keyboard = [
        [
            InlineKeyboardButton("<b>1</b>", callback_data="1"),
            InlineKeyboardButton("<b>2</b>", callback_data="2"),
            InlineKeyboardButton("<b>3</b>", callback_data="3"),
        ],
        [
            InlineKeyboardButton("<b>4</b>", callback_data="4"),
            InlineKeyboardButton("<b>5</b>", callback_data="5"),
            InlineKeyboardButton("<b>6</b>", callback_data="6"),
        ],
        [
            InlineKeyboardButton("<b>7</b>", callback_data="7"),
            InlineKeyboardButton("<b>8</b>", callback_data="8"),
            InlineKeyboardButton("<b>9</b>", callback_data="9"),
        ],
        [InlineKeyboardButton("<b>0</b>", callback_data="0")],
    ]
    return keyboard

def create_difficulty_keyboard() -> list[list[InlineKeyboardButton]]:
    """Create keyboard for difficulty selection with larger text."""
    keyboard = [
        [InlineKeyboardButton("<b>x1-3 Легкий уровень</b>", callback_data="level_easy")],
        [InlineKeyboardButton("<b>x3-6 Средний уровень</b>", callback_data="level_medium")],
        [InlineKeyboardButton("<b>x6-9 Сложный уровень</b>", callback_data="level_hard")],
        [InlineKeyboardButton("<b>x1-9 Полный диапазон</b>", callback_data="level_full")],
    ]
    return keyboard
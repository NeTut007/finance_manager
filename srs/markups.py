import db
from telebot import types

def create_category_keyboard(amount):
    categories = db.get_categories()
    keyboard = types.InlineKeyboardMarkup()
    for category in categories:
        callback_data = f'{category}:{amount}'
        button = types.InlineKeyboardButton(category, callback_data=callback_data)
        keyboard.add(button)
    return keyboard

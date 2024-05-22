from telebot import types
import db

def create_category_keyboard(buttons_per_row=2):
    categories = db.get_categories()
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    
    # Разбить категории на строки по n элементов
    row = []
    for i, category in enumerate(categories):
        row.append(types.KeyboardButton(category))
        if (i + 1) % buttons_per_row == 0 or i == len(categories) - 1:
            keyboard.row(*row)
            row = []

    return keyboard

def get_empty_markup() -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardRemove(selective=True)

def create_inline_category_keyboard(amount):
    categories = db.get_categories()
    keyboard = types.InlineKeyboardMarkup()
    for category in categories:
        callback_data = f"{category}:{amount}"
        keyboard.add(types.InlineKeyboardButton(category, callback_data=callback_data))
    return keyboard

def create_show_transactions_keyboard(categories):
    markup = types.InlineKeyboardMarkup()
    # Добавляем первую кнопку отдельно
    markup.add(types.InlineKeyboardButton("Показать все транзакции", callback_data='show_all_transactions'))
    
    # Добавляем остальные кнопки по две в ряд
    buttons = []
    for category in categories:
        buttons.append(types.InlineKeyboardButton(category, callback_data=f'category_{category}'))
    
    # Разбиваем на строки по две кнопки
    for i in range(0, len(buttons), 2):
        markup.row(*buttons[i:i+2])
    
    return markup
# def get_menu_markup() -> types.ReplyKeyboardMarkup:
#     markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

#     for subject in settings.SUBJECT_LIST:
#         markup.add(
#             types.KeyboardButton(subject.lower().capitalize())
#         )
#     return markup

# def get_cancel_markup() -> types.ReplyKeyboardMarkup:
#     markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#     markup.add(
#             types.KeyboardButton(settings.CANCEL_WORD.lower().capitalize())
#         )
#     return markup

# def get_topics_markup(topics: list) -> types.ReplyKeyboardMarkup:
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     while topics:
#         row = [types.KeyboardButton(topic) for topic in topics[:2]]
#         markup.row(*row)
#         topics = topics[2:]
#     return markup
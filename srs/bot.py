from telebot import types
import telebot
import settings
import db
import logging
from datetime import datetime
import markups

bot = telebot.TeleBot(settings.BOT_TOKEN_DENIS)

@bot.message_handler(commands=['start'])

def send_welcome(message:types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text = 'Hello, I am finance manager helper. \nВведите /help для получения списка команд'
    )
    db.insert_user(message.from_user.username, message.from_user.id)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
    Доступные команды:
/start - начать работу с ботом🐱‍🐉
/help - получить список доступных команд😜
/add_transaction - добавить новую транзакцию 😎
/show_transaction - показать все транзакции👍
/delete_transaction - удалить транзакцию по ID 🌹
/update_transaction - обновить транзакцию ❤
/set_budget - установить бюджет ✔
/show_budgets - показать все бюджеты👀
/update_budget - обновить бюджет 😢
/info_user - инфа о пользователе🎁
    """
    bot.reply_to(message, help_text)


@bot.message_handler(commands=['info_user'])
def info_user(message:types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text = message.chat.first_name
    )

@bot.message_handler(commands=['add_transaction'])
def help_add(message:types.Message):
    am = bot.send_message(
        chat_id=message.chat.id,
        text = 'Введите сумму транзакции'
    )
    bot.register_next_step_handler(am, choose_category) 

def choose_category(message: types.Message):
    try:
        amount = float(message.text)
        msg = bot.send_message(
            chat_id=message.chat.id,
            text='Введите категорию транзакции или выберите из списка:',
            reply_markup=markups.create_inline_category_keyboard(amount)
        )
        # process_custom_category(message,amount,)
    except Exception as error:
        logging.error(f'Пожалуйста, введите числовое значение для суммы: {error}')
        msg = bot.send_message(
            chat_id=message.chat.id,
            text='Пожалуйста, введите числовое значение для суммы:'
        )
        bot.register_next_step_handler(msg, choose_category)

# def process_custom_category(message: types.Message, amount):
#     category = message.text.strip()
#     add_transaction(message, amount, category)

def add_transaction(message: types.Message, amount, category):
    try:
        # Словарь для перевода месяца
        months = {
            'January': 'января', 'February': 'февраля', 'March': 'марта',
            'April': 'апреля', 'May': 'мая', 'June': 'июня',
            'July': 'июля', 'August': 'августа', 'September': 'сентября',
            'October': 'октября', 'November': 'ноября', 'December': 'декабря'
        }
        # Форматируем текущую дату и время
        now = datetime.now()
        month = months[now.strftime('%B')].capitalize()
        date = now.strftime(f"%d {month} %Y, %H:%M")
        db.create_transaction(amount, category, date)
        bot.send_message(message.chat.id, 'Транзакция успешно добавлена 😉')
    except Exception as error:
        logging.error(f'Ошибка при добавлении транзакции: {error}')
        bot.send_message(message.chat.id, 'Произошла ошибка при добавлении транзакции.')

@bot.callback_query_handler(func=lambda call: call.data.startswith('add_trans_'))
def category_step_callback(call:types.CallbackQuery):
    data = call.data.split(':')
    category = data[0].replace('add_trans_', '')
    amount = float(data[1])
    add_transaction(call.message, amount, category)

# Функция для установки бюджета
@bot.message_handler(commands=['set_budget'])   
def set_budget_category(message:types.Message):
    am = bot.send_message(
        chat_id=message.chat.id,
        text='Введите категорию бюджета '
    )
    bot.register_next_step_handler(am, set_budget_amount)
    
def set_budget_amount(message:types.Message):
    category = message.text
    am = bot.send_message(
        chat_id = message.chat.id,
        text='Введите сумму для бюджета'
    )
    bot.register_next_step_handler(am, set_budget_final, category)

def set_budget_final(message:types.Message, category):
    try:
        amount = float(message.text)
        if amount < 0:
            am = bot.send_message(
                chat_id=message.chat.id,
                text=f'Вы ввели отрицательную сумму: {amount} бюджета, попробуйте написать еще раз '
            )
            bot.register_next_step_handler(am, set_budget_final, category)
        else:
            db.set_budgets(category, amount)
            bot.send_message(
                chat_id=message.chat.id,
                text=f'Бюджет создан, у вас есть {amount} рублей на {category}'
            )
    except Exception as error:
        logging.error(f'Был использован не правильный тип данных: {error}')
        am = bot.send_message(
            chat_id=message.chat.id,
            text=f'Нужны числа, а не текст'
        )
        bot.register_next_step_handler(am, set_budget_final, category)

@bot.message_handler(commands=['show_transaction'])
def show_transaction(message: types.Message):
    categories = db.get_all_categories()
    markup = markups.create_show_transactions_keyboard(categories)
    bot.send_message(message.chat.id, "Выберите категорию для просмотра транзакций:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('show_transaction') or call.data == 'show_all_transactions')
def handle_transaction_category_selection(call: types.CallbackQuery):
    if call.data == 'show_all_transactions':
        transactions = db.get_all_transactions()
    else:
        category = call.data.split('category_')[1]
        transactions = db.get_transactions_by_category(category)

    if transactions:
        transactions_text = "\n".join([f"{t[0]}: {t[1]} - {t[2]}" for t in transactions])
    else:
        transactions_text = "Нет транзакций в этой категории."

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=transactions_text)

# Функция для обновления транзакции
@bot.message_handler(commands=['update_transaction'])
def request_transaction_id_for_update(message: types.Message):
    msg = bot.send_message(chat_id=message.chat.id, text="Введите ID транзакции для обновления:")
    bot.register_next_step_handler(msg, update_transaction_step1)

def update_transaction_step1(message: types.Message):
    transaction_id = message.text
    # Проверяем, существует ли такая транзакция
    if db.check_transaction_exists(transaction_id):
        msg = bot.send_message(chat_id=message.chat.id, text="Введите новую сумму:")
        bot.register_next_step_handler(msg, update_transaction_step2, transaction_id)
    else:
        bot.send_message(chat_id=message.chat.id, text="Транзакция не найдена.")

def update_transaction_step2(message: types.Message, transaction_id):
    try:
        new_amount = float(message.text)
        msg = bot.send_message(chat_id=message.chat.id, text="Введите новую категорию:")
        bot.register_next_step_handler(msg, update_transaction_step3, transaction_id, new_amount)
    except ValueError:
        msg = bot.send_message(chat_id=message.chat.id, text="Пожалуйста, введите числовое значение для суммы.")
        bot.register_next_step_handler(msg, update_transaction_step2, transaction_id)

def update_transaction_step3(message: types.Message, transaction_id, new_amount):
    new_category = message.text
    db.update_transaction(transaction_id, new_amount, new_category) 
    bot.send_message(chat_id=message.chat.id, text=f"Транзакция ID {transaction_id} обновлена.")


# @bot.message_handler(func=lambda message: True)
# def Echo(message):
#     bot.reply_to(message, 'Такого нету😁')

logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
    bot.polling()


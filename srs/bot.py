from telebot import types
import telebot
import settings
import db
import logging
from datetime import datetime

bot = telebot.TeleBot(settings.BOT_TOKEN)

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
/balance - отобразить текущий баланс😊
/delete - удалить транзакцию по ID 🌹
/update - обновить транзакцию ❤
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

def choose_category(message:types.Message):
    try:
        amount = float(message.text)
        am = bot.send_message(
            chat_id=message.chat.id,
            text='Введите категорию транзакции'
        )
        bot.register_next_step_handler(am, category_step, amount)
    except Exception as error:
        logging.error(f'Пожалуста введите числовое значение для суммы: {error}')
        am = bot.send_message(
            chat_id=message.chat.id,
            text='Введите числовое значение для суммы '
        )
        bot.register_next_step_handler(am, choose_category)

def category_step(message:types.Message, amount):
    category = message.text
    add_transaction(message, amount, category)
  
def add_transaction(message:types.Message, amount, category):
    try:
        months = {
            'January': 'января', 'February': 'февраля', 'March': 'марта',
            'April': 'апреля', 'May': 'мая', 'June': 'июня',
            'July': 'июля', 'August': 'августа', 'September': 'сентября',
            'October': 'октября', 'November': 'ноября', 'December': 'декабря'
        }
        now = datetime.now()
        month = months[now.strftime('%B')].capitalize() 
        date = now.strftime(f'%d {month} %Y, %H:%M')
        db.create_transactions(amount, category, date) 
        bot.send_message(message.chat.id, 'Транзакция добавлена(☞ﾟヮﾟ)☞')
    except Exception as error:
        logging.error(f'Ошибка при добавлении транзакции: {error}')
        bot.send_message(message.chat.id, 'Не верный формат даты')

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
def show_transaction(message:types.Message):
    transactions = db.get_transactions()
    if transactions:
        response = 'Список всех транзакций: \n'
        for transaction in transactions:
            transaction = list(transaction)
            response += f'ID: {transaction[0]} amount:{transaction[1]} category: {transaction[2]}, date: {transaction[3]}\n'
        bot.send_message(
            chat_id=message.chat.id,
            text=response
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Нет транзакций🎂'
        )




@bot.message_handler(func=lambda message: True)
def Echo(message):
    bot.reply_to(message, 'Такого нету😁')















logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
    bot.polling()
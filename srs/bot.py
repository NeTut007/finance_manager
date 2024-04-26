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
    /add - добавить новую транзакцию (формат: /add сумма категория [дата])😎
    /show - показать все транзакции👍
    /balance - отобразить текущий баланс😊
    /delete - удалить транзакцию по ID (формат: /delete ID)🌹
    /update - обновить транзакцию (формат: /update ID сумма категория дата)❤
    /setbudget - установить бюджет (формат: /setbudget категория сумма)✔
    /showbudgets - показать все бюджеты👀
    /updatebudget - обновить бюджет (формат: /updatebudget ID сумма)😢
    /info_user - инфа о пользователе🎁
    """
    bot.reply_to(message, help_text)


@bot.message_handler(commands=['info_user'])
def info_user(message:types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text = message.chat.first_name
    )

@bot.message_handler(commands=['add'])
def help_add(message:types.Message):
    am = bot.send_message(
        chat_id=message.chat.id,
        text = 'Введите сумму транзакции'
    )
    bot.register_next_step_handler(am, choose_category, message.chat.id) 

def choose_category(message:types.Message, chat_id):
    try:
        amount = float(message.text)
        am = bot.send_message(
            chat_id=message.chat.id,
            text='Введите категорию транзакции'
        )
        bot.register_next_step_handler(am, category_step, amount, chat_id)
    except Exception as error:
        logging.error(f'Пожалуста введите числовое значение для суммы: {error}')
        am = bot.send_message(
            chat_id=message.chat.id,
            text='Введите категорию транзакции'
        )
        bot.register_next_step_handler(am, choose_category, chat_id)

def category_step(message:types.Message, amount, chat_id):
    category = message.text
    bot.send_message(
        chat_id=chat_id,
        text='Транзакция будет добавлена с вашей датой'
    )
    add_transaction(message, amount, category)
  
def add_transaction(message:types.Message, amount, category):
    try:
        date = datetime.now().strftime("%Y-%m-%d")
        db.create_transactions(amount, date , category) 
        bot.send_message(message.chat.id, 'Транзакция добавлена(☞ﾟヮﾟ)☞')
    except Exception as error:
        logging.error(f'Ошибка при добавлении транзакции: {error}')
        bot.send_message(message.chat.id, 'Не верный формат даты')

@bot.message_handler(commands=['set_budget'])
    
def choose_category(message:types.Message):
    try:
        am = bot.send_message(
            chat_id=message.chat.id,
            text='Введите категорию бюджета '
        )
        bot.register_next_step_handler(message, category_step, am)
    except Exception as error:
        logging.error(f'Пожалуста введите числовое значение для суммы: {error}')
        am = bot.send_message(
            chat_id=message.chat.id,
            text='Введите категорию бюджета'
        )
        bot.register_next_step_handler(message, choose_category,am )

def category_step(message:types.Message, chat_id):
    category = message.text
    bot.send_message(
        chat_id=chat_id,
        text='Выбрана категория для бюджета'
    )
    bot.register_next_step_handler(message, choose_amount)
def choose_amount(message:types.Message, chat_id):
    am=bot.send_message(
        chat_id=chat_id,
        text='Введите сумму для бюджета'
    )
    bot.register_next_step_handler(message, choose_step, )


@bot.message_handler(func=lambda message: True)
def Echo(message):
    bot.reply_to(message, 'Такого нету😁')

def hello():













logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
    bot.polling()
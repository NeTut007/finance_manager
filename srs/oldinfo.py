from datetime import datetime

transactions = []
budget = {

}
# Функция для добавления транзакций
def add_transaction (amount,category,date = None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    transactions.append({"amount":amount,'category':category,'date':date})
    # check_budget(category)

# Функция для вывода историй транзакций
def show_transaction ():
    for i in transactions:
        print(f'data:{i['date']},category:{i['category']},amount:{i['amount']}')

# Функиции для подсчета баланса
def general_balance ():
    balance = sum(i ['amount'] for i in transactions)
    return balance

# Функция для экспорта данных в текстовый файл

def export_transactions(name):
    with open(name, 'w', 'utf-8') as file:
        for i in transactions:
            file.write(f'date:{i['date']}, category:{i['category']}, amount:{i['amount']}\n')

# Функция для устнавоки бюджета
def set_budget(category,amount):
    budget[category] = amount

# Функция для проверки превышения бюджета
def check_budget(category):
     if category in budget:
         total_spent = 0
         for i in transactions:
             if i ['category'] == category:
                 total_spent += i ['amount']
         if total_spent < budget[category]:
             print(f'вы близки к привышению бюджета, по категории {category} потрачено уже:{total_spent} бюджет: {budget[category]}')




# x = int(input('Введите сумму пополнения или покупки: '))
# y = input('Введите категорию: ')
# x1 = int(input('Введите сумму пополнения или покупки: '))
# y1 = input('Введите категорию: ')
add_transaction(1000,'зарплата')
add_transaction(-320,'еда')
add_transaction(-500,'еда')
add_transaction(-120000,'техника')
add_transaction(-10000,'техника')
set_budget(amount=-1000, category='eда')
print('история транзакций')
show_transaction()
print('текущий баланс: ',general_balance())
check_budget('еда')
# print(transactions)
# for i in transactions:
#     print(i)
# export_transactions("transactions.txt")






# dict1 = {
#     'category':'category',
#     'amount': 1,
#     'date':'date'
# }
# dict2 = {
#     'category':'category_1',
#     'amount': 2,
#     'date':'date'
# }
# my_list = [dict1,dict2]
# balance = 0
# for i in my_list:
#     balance += i['amount']
# print(balance)


        # bot.register_next_step_handler(msg, process_custom_category, amount)

# @bot.message_handler(commands=['delete_transaction'])
# def delete_transaction_command(message: types.Message):
#     logging.info(f"Команда /delete_transaction от {message.chat.id}")
#     msg = bot.send_message(
#         chat_id=message.chat.id,
#         text='Введите ID транзакции, которую вы хотите удалить'
#     )
#     bot.register_next_step_handler(msg, process_delete_transaction)

# def process_delete_transaction(message: types.Message):
#     try:
#         transaction_id = int(message.text)
#         logging.info(f'Удаление транзакции с ID: {transaction_id}')
#         db.delete_transaction(transaction_id)
#         bot.send_message(message.chat.id, f'Транзакция с ID {transaction_id} успешно удалена.')
#     except ValueError:
#         logging.error(f'Пожалуйста, введите числовое значение для ID транзакции')
#         msg = bot.send_message(
#             chat_id=message.chat.id,
#             text='Пожалуйста, введите числовое значение для ID транзакции:'
#         )
#         bot.register_next_step_handler(msg, process_delete_transaction)
#     except Exception as error:
#         logging.error(f'Ошибка при удалении транзакции: {error}')
#         bot.send_message(message.chat.id, 'Произошла ошибка при удалении транзакции.')



def process_custom_category(message: types.Message, amount):
    category = message.text.strip()
    add_transaction(message, amount, category)
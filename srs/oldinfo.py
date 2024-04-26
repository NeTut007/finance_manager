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
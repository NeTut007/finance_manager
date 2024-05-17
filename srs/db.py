import sqlite3
import os
import logging

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'bot.db')
LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'database_errors.log')

logging.basicConfig(filename=LOG_PATH, level=logging.ERROR, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# функция для создания таблиц
def create_db():
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        table_transaction = '''
            CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
            )
            '''
        table_budgets = '''
            CREATE TABLE IF NOT EXISTS budgets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL
            ) 
            '''
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            user_id INTEGER NOT NULL
        );
        '''
        cursor.execute(table_transaction)
        cursor.execute(table_budgets)
        cursor.execute(create_table_query)
        connection.commit()

    except Exception as error:
        logging.error(f'Ошибка при создании базы данных: {error}')


    finally:
        connection.close()

# функция для удаления таблиц
def drop_tables():
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        delete_table_transaction = 'DROP TABLE IF EXISTS transactions'
        delete_table_budgets = 'DROP TABLE IF EXISTS budgets'
        delete_table_users = 'DROP TABLE IF EXISTS users'
        cursor.execute(delete_table_budgets)
        cursor.execute(delete_table_transaction)
        cursor.execute(delete_table_users)
        connection.commit()
    except Exception as error:
        logging.error(f'Ошибка при удалении таблицы: {error}')
    finally:
        connection.close()

# функция для создания транзакций
def create_transactions(amount, category, date):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        insert_transactions = 'INSERT INTO transactions(amount, category, date) VALUES (?, ?, ?)'
        cursor.execute(insert_transactions, (amount, category, date))
        connection.commit()
    except Exception as error:
        logging.error(f'Ошибка при добавлении транзакции: {error}')
    finally:
        connection.close()

# функция для просмтра всех транзакций
def get_transactions():
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        get_transaction = 'SELECT * FROM transactions'
        cursor.execute(get_transaction)
        ready_transaction = cursor.fetchall()
        return ready_transaction
    except Exception as error:
        logging.error(f'Ошибка при получении транзакции: {error}')
    finally:
        connection.close()

# функция для удаления транзакций
def delete_transactions(transaction_id):
    try:
        connection=sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id))
        connection.commit()
    except Exception as error:
        logging.error(f'Ошибка при удалении транзакции: {error}')
    finally:
        connection.close()

# функция для изменения транзакций
def update_transactions(transaction_id, amount = None, category = None):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        if amount:
            cursor.execute('UPDATE transactions SET amount = ? WHERE id = ?', (amount, transaction_id))
        if category:
            cursor.execute('UPDATE transactions SET category = ? WHERE id = ?', (category, transaction_id))
        connection.commit()
    except Exception as error:
        logging.error(f'Ошибка при  обновлении : {error}')
    finally:
        connection.close()

# функция для просмотра бюджетов
def get_budgets():
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        get_budget = 'SELECT * FROM budgets'
        cursor.execute(get_budget)
        ready_budget = cursor.fetchall()
        return ready_budget
    except Exception as error:
        logging.error(f'Ошибка при получении бюджетов: {error}')
    finally:
        connection.close()

# функция для удаления бюджетов
def delete_budgets(budget_id):
    try:
        connection=sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute('DELETE FROM budgets WHERE id = ?', (budget_id))
        connection.commit()
    except Exception as error:
        logging.error(f'Ошибка при удалении бюджета: {error}')
    finally:
        connection.close()

# функция для изменения бюджета 
def update_budgets(budget_id, amount = None, category = None):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        if amount:
            cursor.execute('UPDATE budgets SET amount = ? WHERE id = ?', (amount, budget_id))
        if category:
            cursor.execute('UPDATE budgets SET category = ? WHERE id = ?', (category, budget_id))
        connection.commit()
    except Exception as error:
        logging.error(f'Ошибка при  обновлении бюджета : {error}')
    finally:
        connection.close()

# функция для установки бюджета 
def set_budgets(category, amount):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        set_budget = ('INSERT INTO budgets (amount, category) VALUES(?,?)')
        cursor.execute(set_budget, (amount, category))
        connection.commit()
    except Exception as error:
        logging.error(f'Ошибка при создании бюджета: {error}')
    finally:
        connection.close()

# Функция, которая добавляет пользователя в базу данных
def insert_user(username:str, user_id:int):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Проверяем, существует ли пользователь с указанным user_id
        select_query = f'''
        SELECT * FROM users
        WHERE user_id = ?;
        '''
        values = (user_id,)
        cursor.execute(select_query, values)

        existing_user = cursor.fetchone()
        if not existing_user:
            insert_query = f'''INSERT INTO users (username, user_id) VALUES (?, ?);'''
            values = (username, user_id)
            cursor.execute(insert_query, values)
            connection.commit()
    finally:
        connection.close()

# функция для проверки id транзакции
def check_id_trasaction(id_transaction):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        select_query = f'SELECT COUNT(*) FROM transactions WHERE id = ?'
        values = (id_transaction,)
        cursor.execute(select_query, values)
        count = cursor.fetchone()[0]
        return count > 0 
    except Exception as error:
        logging.error(f'Ошибка при проверки существования транзакций: {error}')
        return False
    finally:
        connection.close()

# функция для подсчета баланса
def general_balance ():
    transactions = get_transactions()
    nixao=[]
    for transaction in transactions:
        nixao.append(transaction[1])
    balance = sum(nixao)
    return balance

# получать транзакции
def get_categories():
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        select_query = f'SELECT DISTINCT category FROM transactions'
        cursor.execute(select_query)
        categories = [row[0] for row in cursor.fetchall()]
    finally:
        connection.close()
    return categories

#  получать категории бюджетов
def get_categories_for_budget():
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()


        select_query = f'SELECT category FROM transactions'
        cursor.execute(select_query)
        categories = [row[0] for row in cursor.fetchall()]
    finally:
        connection.close()
    return categories
        


        
        



        
        
        
        

# conection = sqlite3.connect('example.db')
# cursor = conection.cursor()
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS users (
#                id INTEGER PRIMARY KEY,
#                name TEXT NOT NULL,
#                age INTEGER NOT NULL
# )
# ''')
 # cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 20)")
 # cursor.execute("INSERT INTO users(name, age) VALUES ('Max', 19),('Alex', 22)")
 # cursor.execute("DELETE FROM users WHERE name = 'Max'")

# cursor.execute("SELECT * FROM users")
# users = cursor.fetchall()
# for i in users:
#     print(i)
# conection.commit()
# conection.close()

if __name__ == '__main__':
    drop_tables()
    create_db()
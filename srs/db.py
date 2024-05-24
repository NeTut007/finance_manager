import sqlite3
import os
import logging

# Определение пути к файлам базы данных и лога
DB_PATH = os.path.join(os.path.dirname(__file__),'..', 'bot.db')
LOG_PATH = os.path.join(os.path.dirname(__file__),'..', 'database_errors.log')

# Настройка логирования
logging.basicConfig(filename=LOG_PATH, level=logging.ERROR, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Функция для создная таблицы с пользователями
def create_table_users():
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        create_table_query = '''
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            user_id INTEGER NOT NULL
        );
        '''
        cursor.execute(create_table_query)
        connection.commit()
        
    finally:
        connection.close()

# Функция для создания таблиц для бюджета и транзакций в БД
def create_db():
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        # Создание таблицы транзакций
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        # Создание таблицы бюджетов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL
            )
        ''')
        connection.commit()
    except Exception as e:
        logging.error(f"Ошибка при создании базы данных: {e}")
    finally:
        connection.close()

# Функция для удаления всех таблиц из БД
def drop_tables():
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        # Удаление таблицы транзакций
        cursor.execute('DROP TABLE IF EXISTS transactions;')
        # Удаление таблицы бюджетов
        cursor.execute('DROP TABLE IF EXISTS budgets;')
        drop_table_query = f'DROP TABLE IF EXISTS users;'
        cursor.execute(drop_table_query)
        connection.commit()
    except Exception as e:
        logging.error(f"Ошибка при удалении таблиц: {e}")
    finally:
        connection.close()

# Функция для добавления новой транзакции
def create_transaction(amount, category, date):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO transactions (amount, category, date) VALUES (?, ?, ?)', (amount, category, date))
        conn.commit()
    except Exception as e:
        logging.error(f"Ошибка при добавлении транзакции: {e}")
    finally:
        conn.close()

# Функция для получения всех транзакций
def get_transactions():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM transactions')
        transactions = c.fetchall()
        return transactions
    except Exception as e:
        logging.error(f"Ошибка при получении транзакций: {e}")
    finally:
        conn.close()

# Функция, проверяющая наличие транзакции в базе данных
def check_transaction_exists(transaction_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Запрашиваем количество записей с указанным ID
        c.execute('SELECT COUNT(*) FROM transactions WHERE id = ?', (transaction_id))
        # Получаем результат запроса
        count = c.fetchone()[0]
        return count > 0
    except Exception as e:
        logging.error(f"Ошибка при проверке существования транзакции: {e}")
        return False
    finally:
        conn.close()

# Функция для удаления транзакции
# Исправил функцию по удалению, чтобы она возвращала или True или False
def delete_transaction(transaction_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
        conn.commit()
        # Проверяем, сколько строк было затронуто последним запросом
        if c.rowcount > 0:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Ошибка при удалении транзакции: {e}")
        return False
    finally:
        conn.close()

# Функция для обновления транзакции
def update_transaction(transaction_id, amount=None, category=None, date=None):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        if amount:
            c.execute('UPDATE transactions SET amount = ? WHERE id = ?', (amount, transaction_id))
        if category:
            c.execute('UPDATE transactions SET category = ? WHERE id = ?', (category, transaction_id))
        if date:
            c.execute('UPDATE transactions SET date = ? WHERE id = ?', (date, transaction_id))
        conn.commit()
    except Exception as e:
        logging.error(f"Ошибка при обновлении транзакции: {e}")
    finally:
        conn.close()

# Функция для установки бюджета
def set_budgets(category, amount):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO budgets (category, amount) VALUES (?, ?)', (category, amount))
        conn.commit()
    except Exception as e:
        logging.error(f"Ошибка при установке бюджета: {e}")
    finally:
        conn.close()

# Функция для получения бюджета
def get_budgets():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM budgets')
        budgets = c.fetchall()
        return budgets
    except Exception as e:
        logging.error(f"Ошибка при получении бюджетов: {e}")
    finally:
        conn.close()

# Функция для обновления установленного бюджета
def update_budget(budget_id, amount):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE budgets SET amount = ? WHERE id = ?', (amount, budget_id))
        conn.commit()
    except Exception as e:
        logging.error(f"Ошибка при обновлении бюджета: {e}")
    finally:
        conn.close()

# Функция для добавления пользователя в БД при запуске бота
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

# Функция для составления списка пользователей из базы данных и отправки в бот админу
def get_users():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        select_query = f'''
        SELECT * FROM users;
        '''
        cursor.execute(select_query)
        user_data = cursor.fetchall()
        results = []
        if user_data:
            for user in user_data:
                
                user_info = {
                    'id': user[0],
                    'username': user[1],
                    'user_id': user[2]
                }
                results.append(user_info)

            return results
    finally:
        conn.close()

def general_balance():
    transactions = get_transactions()  # Предполагается, что функция `get_all_transactions` уже существует
    balance = sum(i['amount'] for i in transactions)
    return balance

def get_categories():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM transactions")
        categories = [row[0] for row in cursor.fetchall()]
    finally:
        conn.close()
    
    return categories

def get_all_categories():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM transactions")
    categories = cursor.fetchall()
    conn.close()
    return [category[0] for category in categories]

def get_all_transactions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT date, category, amount FROM transactions")
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def get_transactions_by_category(category):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT date, category, amount FROM transactions WHERE category = ?", (category,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

if __name__ == '__main__':
    drop_tables()
    create_db()
    create_table_users()
    print('Привет, мой друг!')
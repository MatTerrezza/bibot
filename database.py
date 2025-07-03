import sqlite3
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Настройка подключения к БД
DB_NAME = os.getenv("DB_NAME", "telegram_bot.db")  # Значение по умолчанию

def get_db_connection():
    """Создает и возвращает соединение с базой данных"""
    return sqlite3.connect(DB_NAME)

def init_db():
    """Инициализирует базу данных (создает таблицы)"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Создаем таблицу пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def add_user_if_not_exists(user_id, first_name=None, username=None):
    """
    Добавляет нового пользователя, если он еще не существует
    
    :param user_id: ID пользователя Telegram
    :param first_name: Имя пользователя
    :param username: @username пользователя
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT OR IGNORE INTO users (user_id, first_name, username) 
               VALUES (?, ?, ?)''',
            (user_id, first_name, username)
        )
        conn.commit()

def get_user(user_id):
    """Получает информацию о пользователе по ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()

def get_all_users():
    """Получает список всех пользователей"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM users')
        return [row[0] for row in cursor.fetchall()]

def remove_user(user_id):
    """Удаляет пользователя из базы данных"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        conn.commit()
        return cursor.rowcount > 0

# Инициализация базы данных при импорте модуля
init_db()

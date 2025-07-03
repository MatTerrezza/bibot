import threading
from bot import bot  # Импортируем сам объект бота, а не модуль

if __name__ == "__main__":
    bot_thread = threading.Thread(
        target=bot.polling,  # Теперь обращаемся к методу объекта bot
        kwargs={"none_stop": True}
    )
    bot_thread.start()
    print("Бот запущен!")  # Для проверки

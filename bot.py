import telebot
import buttons
import database
import os
from ai import AIHelper, setup_ai_handlers
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
ADMIN_ID = os.getenv("ADMIN_ID")

with open('company_info.txt', 'r', encoding='utf-8') as file:
    company_info = file.read().strip()

ai_helper = AIHelper(company_info)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    database.add_user_if_not_exists(user_id, message.from_user.username)
    
    welcome_text = (
        f"<b>Telegram-боты и Mini Apps – твой бизнес на автопилоте</b>\n\n"
        f"Привет, {user_name}!\n\n"
        "Ты знаешь, где сейчас твои клиенты? Правильно – в Telegram. И мы поможем тебе построить тут прибыльный бизнес на полном автомате💰\n\n"
        
        "<b>Что мы делаем?</b>\n"
        "🤖Telegram боты – принимают заказы 24/7, отвечают на вопросы и берут оплату,\n"
        "📲Telegram Mini Apps – удобные магазины и сервисы прямо в телеге (без скачивания!),\n"
        "🛠Интеграции – подключим абсолютно все, что важно для работы твоего бизнеса: платежные системы, CRM, AI ассистент, доставка и др сервисы!\n\n"
        
        "<b>Почему это выстрелит?</b>\n"
        "— Клиенты покупают в 3 клика, не выходя из мессенджера,\n"
        "— Ты экономишь на поддержке: бот работает вместо менеджеров,\n"
        "— Продажи растут за счет персонализированных предложений📊\n\n"
        
        "<b>Для кого?</b>\n"
        "🔥 Ритейл и ресейл,\n"
        "📢 Блогеры и эксперты,\n"
        "🚀 Стартапы и малый бизнес,\n"
        "💻 Онлайн-сервисы и SaaS,\n"
        "🎯 Маркетплейсы и агрегаторы,\n"
        "💸 Финтех,\n"
        "🏆 Бизнес, где важен сервис\n\n"
        
        "<b>Как это работает?</b>\n"
        "1. Обсуждаем твой бизнес и цели,\n"
        "2. Создаем решение за 1-2 недели,\n"
        "3. Настраиваем аналитику и масштабирование\n\n"
        
        "<b>Хватит терять клиентов!</b>\n"
        "Получи консультацию и расчет стоимости под твой проект уже сегодня☎️\n\n"
        
        "<i>P.S. Первые результаты уже через месяц. Telegram – не просто мессенджер, а твой новый канал продаж. Используй его на 100%!</i>"
    )

    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=buttons.get_main_keyboard(),
        parse_mode='HTML'
    )

@bot.message_handler(func=lambda m: m.text == "Связаться со мной")
def send_me(message):
    bot.send_message(message.chat.id, "Написать мне: https://t.me/matterrezza")

@bot.message_handler(func=lambda m: m.text == "Оформить заказ через форму")
def send_form(message):
    bot.send_message(
        message.chat.id,
        "Нажмите на кнопку ниже",
        reply_markup=buttons.get_inline_keyboard()
    )
    
@bot.message_handler(func=lambda m: m.text == "Услуги")
def send_serv(message):
    bot.send_message(
        message.chat.id,
        "👇 <b>Выберите услугу:</b>",
        reply_markup=buttons.get_inline_menu(),
        parse_mode='HTML'
    )
    
@bot.callback_query_handler(func=lambda call: True)
def handle_services(call):
    if call.data == 'service_bots':
        text = """<b>🤖 Разработка Telegram-ботов</b>

Полная автоматизация вашего бизнеса:
• Прием заказов 24/7
• Интеграция с платежами
• Умные рекомендации для клиентов
• Готовое решение за 3-5 дней"""
        
    elif call.data == 'service_scripts':
        text = """<b>🐍 Python-скрипты</b>

Скрипты для любых задач:
• Парсинг сайтов и данных
• Автоматизация отчетов и Excel
• Интеграции между сервисами
• Боты для внутренних процессов
• Решение за 1-3 дня с гарантией"""
        
    elif call.data == 'service_crm':
        text = """<b>🛠 Настройка CRM</b>

Настроим Bitrix24 под ваш бизнес:
• Автоматизация продаж и задач
• Интеграция с сайтом и соцсетями
• Воронки продаж и CRM-аналитика
• Обучение сотрудников работе с системой
• Готовые решения за 2-3 дня"""
        
    elif call.data == 'service_miniapps':
        text = """<b>📱 Mini Apps</b>

Мобильные приложения прямо в Telegram!
• Полноценные магазины без скачивания
• Быстрая загрузка и удобный интерфейс
• В 3 раза дешевле мобильных приложений
• Поддержка платежей и уведомлений
• Примеры работ в портфолио"""
        
    elif call.data == 'back_to_main':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="👇 <b>Выберите услугу:</b>",
            reply_markup=buttons.get_inline_menu(),
            parse_mode='HTML'
        )
        return
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=buttons.get_back_button(),
        parse_mode='HTML'
    )

# Подключаем AI обработчики
setup_ai_handlers(bot, ai_helper)

if __name__ == '__main__':
    bot.polling(none_stop=True)

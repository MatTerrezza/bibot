import requests

# ======== НАСТРОЙКИ ========
OPENROUTER_API_KEY = "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"
DEEPMODEL = "deepseek/deepseek-chat-v3-0324:free"
KNOWLEDGE_FILE = "knowledge.txt"
MAX_HISTORY = 5  # Максимальное количество сообщений в истории

# ======== ИНИЦИАЛИЗАЦИЯ ========
conversation_history = []

# ======== ЗАГРУЗКА БАЗЫ ЗНАНИЙ ========
def load_knowledge():
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        return f.read()

# ======== ЗАПРОС К DEEPSEEK ========


def ask_deepseek(user_query):
    global conversation_history
    
    # Загружаем базу знаний
    knowledge = load_knowledge()
    
    # Формируем промт с историей
    system_prompt = f"""
    Ты — ИИ-консультант который должен отвечать как человек и делать так чтобы клиент захотел заказать мои УСЛУГИ под ключ ты не должен давать полную инструкцию по выполнению. Отвечай ТОЛЬКО на основе предоставленной информации.
    Учитывай историю диалога. Если ответа нет в данных, скажи: «Информация не найдена». Сообщения не должны содержать лишних символов вроде ** или галочек, стрелок

    База знаний:
    {knowledge}
    """
    
    # Добавляем текущий вопрос в историю
    conversation_history.append({"role": "user", "content": user_query})
    
    # Ограничиваем историю
    if len(conversation_history) > MAX_HISTORY:
        conversation_history = conversation_history[-MAX_HISTORY:]
    
    # Формируем полный список сообщений
    messages = [
        {"role": "system", "content": system_prompt},
        *conversation_history
    ]
    
    # Отправляем запрос
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Consultant",
    }
    
    data = {
        "model": DEEPMODEL,
        "messages": messages,
        "temperature": 0.5,  # Средний уровень креативности
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        ai_response = response.json()["choices"][0]["message"]["content"]
        # Добавляем ответ ИИ в историю
        conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response
    else:
        return f"Ошибка API: {response.text}"

# ======= Соеденение с тг ботом =======

class AIHelper:
    def __init__(self, company_info: str):
        self.company_info = company_info

    def get_response(self, user_query: str) -> str:
        # Используем существующую функцию ask_deepseek
        return ask_deepseek(user_query)

def setup_ai_handlers(bot_instance=None, ai_helper=None):
    if bot_instance:  # Режим работы с Telegram-ботом
        @bot_instance.message_handler(func=lambda message: True)
        def handle_ai_questions(message):
            if message.text.startswith('/') or message.text in [
                "Связаться со мной",
                "Оформить заказ через форму",
                "Услуги",
                "Консультация"
            ]:
                return
                
            bot_instance.send_chat_action(message.chat.id, 'typing')
            response = ask_deepseek(message.text)
            bot_instance.reply_to(message, response)
    else:  # Консольный режим
        print("🤖 ИИ-консультант готов! (Для выхода введите 'exit')")
        while True:
            query = input("\nВаш вопрос: ").strip()
            if query.lower() in ["exit", "выход"]:
                break
            answer = ask_deepseek(query)
            print("\nОтвет:", answer)

        # Отправляем "Печатает..." статус
        bot_instance.send_chat_action(message.chat.id, 'typing')
        
        # Получаем ответ от AI
        response = ai_helper.get_response(message.text)
        
        # Отправляем ответ
        bot_instance.reply_to(message, response)

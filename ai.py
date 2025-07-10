import os
import openai
import logging
from typing import Optional

class AIHelper:
    def __init__(self, company_info: str):
        self.company_info = company_info
        self.client = None
        self._init_openai()

    def _init_openai(self):
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            
            openai.api_key = api_key
            self.client = openai.OpenAI()
            logging.info("OpenAI client initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize OpenAI: {e}")
            self.client = None

    def generate_response(self, user_message: str) -> Optional[str]:
        if not self.client:
            return "Сервис временно недоступен. Пожалуйста, попробуйте позже."

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"Ты консультант компании. Отвечай только по информации о компании. Информация о компании:\n{self.company_info}"
                    },
                    {
                        "role": "user", 
                        "content": user_message
                    }
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"AI request failed: {e}")
            return "Произошла ошибка при обработке запроса"

def setup_ai_handlers(bot, ai_helper):
    @bot.message_handler(func=lambda m: True)
    def handle_all_messages(message):
        if message.text and not message.text.startswith('/'):
            response = ai_helper.generate_response(message.text)
            bot.send_message(message.chat.id, response)

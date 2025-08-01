import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Тестовый запрос"}]
    )
    print("OpenAI работает корректно!")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Ошибка OpenAI: {type(e).__name__}: {e}")

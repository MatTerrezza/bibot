import telebot.types as types
import json
import os

def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    btn_form = types.KeyboardButton("Оформить заказ через форму")
    btn_me = types.KeyboardButton("Связаться со мной")
    btn_service = types.KeyboardButton("Услуги")
    
    keyboard.add(btn_service)
    keyboard.add(btn_form, btn_me)
    return keyboard

def get_inline_menu():
    markup = types.InlineKeyboardMarkup()
    
    btn1 = types.InlineKeyboardButton("🤖 Telegram-боты", callback_data='service_bots')
    btn2 = types.InlineKeyboardButton("📱 Mini Apps", callback_data='service_miniapps')
    btn3 = types.InlineKeyboardButton("🛠 Настройка CRM", callback_data='service_crm')
    btn4 = types.InlineKeyboardButton("🐍 Python-скрипты", callback_data='service_scripts')    
    
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def get_back_button():
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')
    markup.add(btn_back)
    return markup
    
def get_inline_keyboard():
    inline_keyboard = types.InlineKeyboardMarkup()
    btn_lform = types.InlineKeyboardButton(
        text="Заполнить форму", 
        url="https://docs.google.com/forms/d/1xVZFQK6DF6OOVr9dgB03_zK96myFYJf9FNiGEGffMCE/edit"
    )
    
    inline_keyboard.add(btn_lform)
    return inline_keyboard

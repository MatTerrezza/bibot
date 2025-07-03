import telebot.types as types
import json
import os

def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_form = types.KeyboardButton("Оформить заказ через форму")
    btn_me = types.KeyboardButton("Связаться со мной")
    
    keyboard.add(btn_form, btn_me)
    return keyboard

def get_inline_keyboard():
    inline_keyboard = types.InlineKeyboardMarkup()
    btn_lform = types.InlineKeyboardButton(
        text="Заполнить форму", 
        url="https://docs.google.com/forms/d/1xVZFQK6DF6OOVr9dgB03_zK96myFYJf9FNiGEGffMCE/edit"
    )
    
    inline_keyboard.add(btn_lform)
    return inline_keyboard

import telebot
from telebot import types
import json
from geopy import geocoders
from os import environ
bot = telebot.TeleBot("6215381559:AAEThVyZ-HYwlQfXkpLJAmWovz4lghUQ8zc")
token_accu=environ["2wxoy7OiAMS5Wea588ib4mwO7WjGZ3V5"]
token_yandex=environ["7452afd2-2932-488b-9d6e-02a2e8437274"]


@bot.message_handler(content_types=['text'])#!!!

def get_text_messages(message):

    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = "Привет, хочешь прислать мне свой гардероб? Я могу посоветовать, в чем сегодня лучше выйти на улицу"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.register_next_step_handler (get_cloth)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'До встречи!')

def get_cloth(shtyka, temp,  message):
    bot.send_message(message.from_user.id, 'Напиши что это за вещь')
    shtyka=message.text
    bot.send_message(message.from_user.id, 'напиши насколько вещь теплая : )')
    temp = message.text

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = "Это все?"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker1(call, message):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Я запомню')
    elif call.data == "no":
        bot.register_next_step_handler(message, get_cloth)

def website(message):
    ma = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    photo1 = types.KeyboardButton('/photo1')
    photo2 = types.KeyboardButton('photo2')
    ma.add(photo1, photo2)
    bot.send_message(message.chat.id, "l2", reply_markup=ma)



bot.polling(none_stop=True, interval=0)


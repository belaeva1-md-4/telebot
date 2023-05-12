import telebot
from pyowm import OWM
from telebot import types

bot = telebot.TeleBot("6215381559:AAEThVyZ-HYwlQfXkpLJAmWovz4lghUQ8zc")
@bot.message_handler(commands=['start']) #реакция на команду
def get_text_messages(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)  # наша клавиатура
    key_yes = types.KeyboardButton(text='Да')
    key_no = types.KeyboardButton(text='Пока')
    key_get = types.KeyboardButton(text='Хочу получить подборку')
    keyboard.add(key_no, key_yes, key_get)
    bot.send_message(message.chat.id, 'Привет, хочешь прислать мне свой гардероб? Я могу посоветовать, в чем сегодня лучше выйти на улицу', reply_markup=keyboard)

@bot.message_handler(content_types=['text']) #реакйия на любой текст, выполняется один раз
def otvet(message):
    if (message.text=='Да'):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False,
                                             one_time_keyboard=True)
        key1 = types.KeyboardButton(text='Куртка')
        key2 = types.KeyboardButton(text='Штаны')
        key3 = types.KeyboardButton(text='Обувь')
        key4 = types.KeyboardButton(text='Футболка/Тонкий низ')
        key5 = types.KeyboardButton(text='Свитер')
        key6 = types.KeyboardButton(text='Юбка')
        keyboard.add(key1, key2, key3, key4, key5, key6)
        msg=bot.send_message(message.chat.id, text="К какой категории можно отнести эту вещь?", reply_markup=keyboard)
        bot.register_next_step_handler(msg, otvet1) #Запомни как ты с этим ебалась и запомни (после получения ответа(кнопки) переходим)
    elif (message.text=="Пока"):
        bot.send_message(message.chat.id, text="До встречи")

def otvet1(message):
    if (message.text == 'Куртка') or (message.text == 'Штаны') or (message.text == 'Обувь'):
        verh(message)
    elif (message.text=="Свитер"):
        sweater(message)
    elif(message.text=="Футболка/Тонкий низ"):
        shirt(message)

def verh(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False,
                                         one_time_keyboard=True)
    key1 = types.KeyboardButton(text='Зимняя')
    key2 = types.KeyboardButton(text='Летняя')
    key3 = types.KeyboardButton(text='Осень-весна')
    keyboard.add(key1, key2, key3)
    msg=bot.send_message(message.chat.id, text="В какое время года вы носите эту вещь?", reply_markup=keyboard)
    bot.register_next_step_handler(msg, jacket1)

def jacket1(message):
    if (message.text=='Зимняя'):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False,
                                             one_time_keyboard=True)
        key1 = types.KeyboardButton(text='В сильные холода')
        key2 = types.KeyboardButton(text='В обычную температуру')
        key3 = types.KeyboardButton(text='В теплые дни')
        keyboard.add(key1, key2, key3)
        msg=bot.send_message(message.chat.id, text="В какую температуру обычно носите?", reply_markup=keyboard)
        bot.register_next_step_handler(msg, zap)

    elif (message.text=='Летняя'):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False,
                                             one_time_keyboard=True)
        key1 = types.KeyboardButton(text='Холодное лето')
        key2 = types.KeyboardButton(text='Норм')
        key3 = types.KeyboardButton(text='Когда жарко')
        keyboard.add(key1, key2, key3)
        msg=bot.send_message(message.chat.id, text="В какую температуру обычно носите?", reply_markup=keyboard)
        bot.register_next_step_handler(msg, zap)

    elif (message.text == 'Осень-весна'):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False,
                                             one_time_keyboard=True)
        key1 = types.KeyboardButton(text='Холод')
        key2 = types.KeyboardButton(text='Норм')
        key3 = types.KeyboardButton(text='Когда жарко')
        keyboard.add(key1, key2, key3)
        msg=bot.send_message(message.chat.id, text="В какую температуру обычно носите?", reply_markup=keyboard)
        bot.register_next_step_handler(msg, zap)


def sweater(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False,
                                         one_time_keyboard=True)
    key1 = types.KeyboardButton(text='Теплый')
    key2 = types.KeyboardButton(text='Обычный')
    key3 = types.KeyboardButton(text='Тонкий')
    keyboard.add(key1, key2, key3)
    msg = bot.send_message(message.chat.id, text="Насколько он теплый?", reply_markup=keyboard)
    bot.register_next_step_handler(msg, zap)

def shirt(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False,
                                         one_time_keyboard=True)
    key1 = types.KeyboardButton(text="Плотная")
    key2 = types.KeyboardButton(text='Обычный')
    key3 = types.KeyboardButton(text='Тонкий')
    keyboard.add(key1, key2, key3)
    msg = bot.send_message(message.chat.id, text="Насколько плотная вещь?", reply_markup=keyboard)
    bot.register_next_step_handler(msg, zap)

def zap(message):
    bot.send_message(message.chat.id, text="Запомню")



bot.polling(none_stop=True, interval=0)
#Привязка к врпемени года
#Среднестатестическая темп - обычная погода
#Несколько подборок
#Изменить данные
#Где-то хранить данные??*
#Реализовать обучение???*

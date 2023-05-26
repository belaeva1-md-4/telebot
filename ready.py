import telebot
from telebot import types
import sqlite3
from pyowm import OWM
bot = telebot.TeleBot("6215381559:AAEThVyZ-HYwlQfXkpLJAmWovz4lghUQ8zc")
name=None
item=None
catg=None
vremyagoda=None
temp=None



@bot.message_handler(commands=['start']) #реакция на команду
def get_text_messages(message):
    global name
    connection=sqlite3.connect('db.sql')
    cursor=connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), item varchar(50), category varchar(50), vremyagoda varchar(50), temp varchar(50))')
    connection.commit()# *много мата*
    cursor.close()
    connection.close()

    name=message.from_user.first_name
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)  # наша клавиатура
    key_yes = types.KeyboardButton(text='Да')
    key_no = types.KeyboardButton(text='Пока')
    key_get = types.KeyboardButton(text='Хочу получить подборку на сегодня')
    key_pogoda = types.KeyboardButton(text='Хочу узнать погоду')
    keyboard.add(key_no, key_yes, key_get, key_pogoda)
    bot.send_message(message.chat.id, 'Привет, ' +name + '! Xочешь прислать мне свой гардероб? Я могу посоветовать, в чем сегодня лучше выйти на улицу', reply_markup=keyboard)

@bot.message_handler(content_types=['text']) #реакйия на любой текст, выполняется один раз
def otvet(message):
    if (message.text=='Да'):
        #cursor.execute(f'ALTER TABLE users ADD COLUMN item varchar')#!@!!!! сделать так, чтобы польз был тут один раз!!! try?
        msg=bot.send_message(message.chat.id, text="Назовите как нибудь эту вещь")
        bot.register_next_step_handler(msg, category)
    elif (message.text=="Пока"):
        bot.send_message(message.chat.id, text="До встречи!")
    elif (message.text=="Хочу получить подборку на сегодня"):
        print("хз пока")
    elif (message.text=="Хочу узнать погоду"):
        get_text_messages(message)




def category(message):
    global item
    item= message.text
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
    key1 = types.KeyboardButton(text='Куртка')
    key2 = types.KeyboardButton(text='Штаны')
    key3 = types.KeyboardButton(text='Обувь')
    key4 = types.KeyboardButton(text='Футболка/Тонкий низ')
    key5 = types.KeyboardButton(text='Свитер')
    key6 = types.KeyboardButton(text='Юбка')
    keyboard.add(key1, key2, key3, key4, key5, key6)
    msg = bot.send_message(message.chat.id, text="К какой категории можно отнести эту вещь?", reply_markup=keyboard)
    bot.register_next_step_handler(msg, otvet1)  # Запомни как ты с этим ебалась и запомни (после получения ответа(кнопки) переходим)

def otvet1(message):
    global catg
    catg=message.text
    if (message.text == 'Куртка') or (message.text == 'Штаны') or (message.text == 'Обувь'):
        verh(message)
    elif (message.text=="Свитер"):
        sweater(message)
    elif(message.text=="Футболка/Тонкий низ"):
        shirt(message)
    elif (message.text=="Юбка"):
        connection = sqlite3.connect('db.sql')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users(name, item, category) VALUES (?, ?, ?)',
                       (name, item, catg,))  # добавляем все одним действием иначе смерть
        connection.commit()
        cursor.close()
        connection.close()
        bot.send_message(message.chat.id, text="Запомню!")


def verh(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
    key1 = types.KeyboardButton(text='Зимняя')
    key2 = types.KeyboardButton(text='Летняя')
    key3 = types.KeyboardButton(text='Осень-весна')
    keyboard.add(key1, key2, key3)
    msg=bot.send_message(message.chat.id, text="В какое время года вы носите эту вещь?", reply_markup=keyboard)
    bot.register_next_step_handler(msg, jacket1)
def jacket1(message):
    global vremyagoda
    vremyagoda = message.text
    if (message.text=='Зимняя'):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False,
                                             one_time_keyboard=True)
        key1 = types.KeyboardButton(text='В сильные холода')
        key2 = types.KeyboardButton(text='В обычную температуру')
        key3 = types.KeyboardButton(text='В теплые дни')
        keyboard.add(key1, key2, key3)
        msg=bot.send_message(message.chat.id, text="В какую температуру обычно носите?", reply_markup=keyboard)
        bot.register_next_step_handler(msg, add)

    elif (message.text=='Летняя'):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False,
                                             one_time_keyboard=True)
        key1 = types.KeyboardButton(text='Холодное лето')
        key2 = types.KeyboardButton(text='Норм')
        key3 = types.KeyboardButton(text='Когда жарко')
        keyboard.add(key1, key2, key3)
        msg=bot.send_message(message.chat.id, text="В какую температуру обычно носите?", reply_markup=keyboard)
        bot.register_next_step_handler(msg, add)

    elif (message.text == 'Осень-весна'):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False,
                                             one_time_keyboard=True)
        key1 = types.KeyboardButton(text='Холод')
        key2 = types.KeyboardButton(text='Норм')
        key3 = types.KeyboardButton(text='Когда жарко')
        keyboard.add(key1, key2, key3)
        msg=bot.send_message(message.chat.id, text="В какую температуру обычно носите?", reply_markup=keyboard)
        bot.register_next_step_handler(msg, add)


def sweater(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False,
                                         one_time_keyboard=True)
    key1 = types.KeyboardButton(text='Теплый')
    key2 = types.KeyboardButton(text='Обычный')
    key3 = types.KeyboardButton(text='Тонкий')
    keyboard.add(key1, key2, key3)
    msg = bot.send_message(message.chat.id, text="Насколько он теплый?", reply_markup=keyboard)
    bot.register_next_step_handler(msg, add_other)



def shirt(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False,
                                         one_time_keyboard=True)
    key1 = types.KeyboardButton(text="Плотная")
    key2 = types.KeyboardButton(text='Обычный')
    key3 = types.KeyboardButton(text='Тонкий')
    keyboard.add(key1, key2, key3)
    msg = bot.send_message(message.chat.id, text="Насколько плотная вещь?", reply_markup=keyboard)
    bot.register_next_step_handler(msg, add_other)
def add_other(message):
    global temp
    temp = message.text
    connection = sqlite3.connect('db.sql')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users(name, item, category, temp) VALUES (?, ?, ?, ?)',
                   (name, item, catg, temp,))  # добавляем все одним действием и запятую иначе смерть
    connection.commit()
    cursor.close()
    connection.close()
    bot.send_message(message.chat.id, text="Запомню!")


def add(message):
    global temp
    temp=message.text
    connection = sqlite3.connect('db.sql')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users(name, item, category, vremyagoda, temp) VALUES (?, ?, ?, ?, ?)',
                   (name, item, catg, vremyagoda, temp,))  # добавляем все одним действием и запятую иначе смерть
    connection.commit()
    cursor.close()
    connection.close()
    bot.send_message(message.chat.id, text="Запомню!")

#написать алгоритм обработки






#погода

def get_location(lat, lon):
    url=f"https://yandex.ru/pogoda/maps/nowcast?lat={lat}&lon={lon}&via=hnav&le_Lightning=1"
    return url

def weather(city: str):
    owm=OWM("482833602a3b416d53c156c563297579")
    mgr=owm.weather_manager()
    observation=mgr.weather_at_place(city)
    weather=observation.weather
    location=get_location(observation.location.lat, observation.location.lon)
    temperature=weather.temperature("celsius")
    return temperature, location

def get_text_messages(message):
    bot.send_message(message.from_user.id, "Введите название города")
    bot.register_next_step_handler(message, get_weather)

seg=None
def get_weather(message):
    city=message.text
    global seg
    try:
        w=weather(city)
        bot.send_message(message.from_user.id, f"В городе {city} сейчас {round( w[0]['temp'] ) } градусов, "f" чувствуется как {round(w[0]['feels_like'])} градусов")
        seg=str({round(w[0]['feels_like'])})
        bot.send_message(message.from_user.id, "Введите название города")
        bot.register_next_step_handler(message, get_weather)
    except Exception:
        bot.send_message(message.from_user.id, "Такого города нет в базе")
        bot.send_message(message.from_user.id,"Введите название города")
        bot.register_next_step_handler(message, get_weather)


def sort():
    connection=sqlite3.connect('db.sql')
    cursor=connection.cursor()
    #cursor.execute("SELECT 'name' FROM 'users' WHERE '' = ?", (name,))
    #connection.commit()
    cursor.execute('SELECT * FROM users')
    users=cursor.fetchall()
    polz=[]
    for el in users:
        if {el[1]}==name:
            polz.append(el[1])
    print(*polz)


    '''while True:
        stroka = cursor.fetchone()
        if stroka:
            print(stroka)
        else:
            break'''
    cursor.close()
    connection.close()

sort()






bot.polling(none_stop=True, interval=0)

#Привязка к врпемени года
#Среднестатестическая темп - обычная погода
#Несколько подборок
#Изменить данные
#Где-то хранить данные??*
#Реализовать обучение???*
#рассылка

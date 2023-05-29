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
        get_text_messages1(message)
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
    key7=types.KeyboardButton(text='Назад')
    keyboard.add(key1, key2, key3, key4, key5, key6, key7)
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
    elif (message.text=="Назад"):
        get_text_messages(message)


def verh(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
    key1 = types.KeyboardButton(text='Зимняя')
    key2 = types.KeyboardButton(text='Летняя')
    key3 = types.KeyboardButton(text='Осень-весна')
    key4 = types.KeyboardButton(text='Назад')
    keyboard.add(key1, key2, key3, key4)
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
    elif (message.text == "Назад"):
        category(message)


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


def get_weather(message):
    city=message.text
    try:
        w=weather(city)
        bot.send_message(message.from_user.id, f"В городе {city} сейчас {round( w[0]['temp'] ) } градусов, "f" чувствуется как {round(w[0]['feels_like'])} градусов")
        pog=str({round(w[0]['feels_like'])})
        bot.send_message(message.from_user.id, "Введите название города")
        bot.register_next_step_handler(message, get_weather)
    except Exception:
        bot.send_message(message.from_user.id, "Такого города нет в базе")
        bot.send_message(message.from_user.id,"Введите название города")
        bot.register_next_step_handler(message, get_weather)

def get_text_messages1(message):
    bot.send_message(message.from_user.id, "Введите название города")
    bot.register_next_step_handler(message, get_weather1)

pog=None
def get_weather1(message):
    city=message.text
    global pog
    w=weather(city)
    pog=str({round(w[0]['feels_like'])})
    sort_po_polz(message)

def sort_po_polz(message):
    name='Tovarish zamaetov'
    connection=sqlite3.connect('db.sql')
    cursor=connection.cursor()
    cursor.execute('SELECT * FROM users')
    users=cursor.fetchall()
    polz=[]
    for el in users:
        if el[1]==name:
            polz.append(el)
    kurtka=[]
    obuv = []
    shirt = []
    sweater = []
    skirt = []
    footb = []
    for el in polz:
        if el[3]=='Куртка':
            kurtka.append(el[3])
        if el[3]=='Обувь':
            obuv.append(el[3])
        if el[3]=='Штаны':
            shirt.append(el[3])
        if el[3]=='Свитер':
            sweater.append(el[3])
        if el[3]=='Юбка':
            skirt.append(el[3])
        if el[3]=='Футболка/Тонкий низ':
            footb.append(el[3])
    cursor.close()
    connection.close()

    algo(kurtka, message)


def algo(kurtka, message):#сделать связь с погодой!!!
    k_pod=[]
    print(int(pog))
    for el in kurtka:
        if el[3]=="Куртка":
            if pog<-20:
                for el in kurtka:
                    if el[4]=='Сильные холода':
                        k_pod.append(el[2])
            elif -20<pog<-10:
                for el in kurtka:
                    if el[4] == 'В обычную температуру':
                        k_pod.append(el[2])
            elif -10<pog<0:
                for el in kurtka:
                    if el[4] == 'В теплые дни':
                        k_pod.append(el[2])
    print(*k_pod)

    '''elif el[3] == "Штаны":
        if el[4] == "Зимняя":
            if el[5]== 'В сильные холода':
                a=25
                if S not in N:S+=a
            elif el[5]=='В обычную температуру':
                a=20
                if S not in N:S+=a
            elif el[5] =='В теплые дни':
                a=15
                if S not in N: S += a
        #elif el[4] == "Летняя":

        #elif el[4] == "Осень-Весна":
    elif el[3] == "Обувь":
        if el[4] == "Зимняя":
            if el[5] == 'В сильные холода':
                a = 25
                if S not in N: S += a
            elif el[5] == 'В обычную температуру':
                a = 20
                if S not in N: S += a
            elif el[5] == 'В теплые дни':
                a = 15
                if S not in N: S += a'''
    #bot.send_message(message.chat.id, f"Сегодня {pog} градусов. Можно надеть " + k_pod[0])






bot.polling(none_stop=True, interval=0)

#Привязка к врпемени года
#Среднестатестическая темп - обычная погода
#Несколько подборок
#Изменить данные
#Где-то хранить данные??*
#Реализовать обучение???*
#рассылка
#взять среднестат темп страны+отталкиваться от нее
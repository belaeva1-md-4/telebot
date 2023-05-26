import telebot
from pyowm import OWM
bot = telebot.TeleBot("6215381559:AAEThVyZ-HYwlQfXkpLJAmWovz4lghUQ8zc")

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

@bot.message_handler(content_types=['text'])#!!!
def get_text_messages(message):
    if message.text=="/weather":
        bot.send_message(message.from_user.id, "Введите название города")
        bot.register_next_step_handler(message, get_weather)
    else:
        bot.send_message(message.from_user.id, "Напиши /weather")


def get_weather(message):
    city=message.text
    try:
        w=weather(city)
        bot.send_message(message.from_user.id, f"В городе {city} сейчас {round( w[0]['temp'] ) } градусов, "f" чувствуется как {round(w[0]['feels_like'])} градусов")
        print(round(w[0]['feels_like']))
        seg=str({round(w[0]['feels_like'])})
        bot.send_message(message.from_user.id, "Введите название города")
        bot.register_next_step_handler(message, get_weather)
    except Exception:
        bot.send_message(message.from_user.id, "Такого города нет в базе")
        bot.send_message(message.from_user.id,"Введите название города")
        bot.register_next_step_handler(message, get_weather)

bot.polling(none_stop=True, interval=0)

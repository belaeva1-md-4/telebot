import telebot
from dispatcher import db
from копия import botBase
botBase=botBase('db')
bot = telebot.TeleBot("...")







import sqlite3
class dorDB:
    def __init__(self, db_file):
        #инициализация соединения с БД
        self.connect = sqlite3.connect(db_file)
        self.cursor=self.connect.cursor()
    def user_exists(self, user_id):
        # проверка есть ли юзер в БД
        result=self.cursor.execute("SELECT 'id' FROM 'users WHERE 'user_id' = ?", (user_id,))
        return bool(len(result.fetchall()))
    def get_user_id(self, user_id):
        #получаем id юзера в базе по его user_id в телеграмме
        result=self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'user_id' =  ?", (user_id))
        return result.fetchone()[0]
    def add_user(self, user_id):
        #добавляем юзера в БД
        self.cursor.execute("INSERT  INTO 'users' ('user_id') VALUES (?)", (user_id,))
        return self.connect.commit()
    async def add(item):
        m=[]
        m.append(item)
        cursor = connect.cursor()
        cursor.execute('INSERT INTO ')

    def close(self):
        self.connect.close()


 #connection=sqlite3.connect('db.sql')
    #cursor=connection.cursor()
    #cursor.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50)), item varchar, category varchar, vremyagoda varchar, temp varchar')
    #connection.commit()



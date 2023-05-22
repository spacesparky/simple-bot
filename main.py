import psycopg2
import telebot
import datetime
from telebot import types

token = "6237295485:AAHN28fR6ikV1CbWbbYN7d7aLDL703O4rvI" #token

bot = telebot.TeleBot(token)

conn = psycopg2.connect(database="schedule_db",
                        user="postgres",
                        password="1",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


def week():
    week_number = datetime.datetime.today().isocalendar()[1]
    parity = week_number % 2
    return parity


def get_shedule(day, week):
    if day == 1:
        day = 'ПОНЕДЕЛЬНИК'
    elif day == 2:
        day = 'ВТОРНИК'
    elif day == 3:
        day = 'СРЕДА'
    elif day == 4:
        day = 'ЧЕТВЕРГ'
    elif day == 5:
        day = 'ПЯТНИЦА'
    cursor.execute("SELECT * FROM timetable where day = %s and even = %s", (day, week))
    records = list(cursor.fetchall())
    schedule = '--------------------------------------\n' \
              '|            '+day+'           |\n' \
              '--------------------------------------\n'
    for i in range(0,5):
        found = False
        for x in range(len(records)):
            cursor.execute(f"SELECT full_name FROM teacher where subject = '{records[x][2]}'")
            teacher = cursor.fetchone()
            if records[x][6] == i+1:
                schedule += f'{records[x][4]} ' + f'{records[x][2]}' + ' кабинет-' + f'{records[x][3]}' +' преподаватель -'  + f'{teacher[0]}\n'
                found = True
                break
        if not found:
            schedule += '<нет пары>\n'
    return schedule


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Хочу", "/help", "/today", "/monday","/tuesday","/wednesday","/thursday","/friday","/week","/weekscedule", "/nextweekscedule")
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать свежую информацию о МТУСИ?', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'я вывожу расписание по вашему запросу\n'
                                      '/today -расписание на сегодня\n'
                                      '/monday - расписание на понедельник этой недели\n'
                                      '/tuesday - расписание на вторник этой недели\n'
                                      '/wednesday - расписание на среду этой недели\n'
                                      '/thursday - расписание на четверг этой недели\n'
                                      '/friday - расписание на пятницу этой недели\n'
                                      '/week - четность или нечетность текущей недели\n'
                                      '/weekscedule -расписание на неделю\n'
                                      '/nextweekscedule -расписание на следующую неделю\n')


@bot.message_handler(commands=['week'])
def week_message(message):
    if week() == 0:
        bot.send_message(message.chat.id, 'неделя четная')
    else:
        bot.send_message(message.chat.id, 'неделя нечетная')


@bot.message_handler(commands=['today'])
def monday(message):
    if datetime.datetime.today().isoweekday() == 1 or datetime.datetime.today().isoweekday() == 2:
        bot.send_message(message.chat.id,'сегодня выходной')
    else:
        bot.send_message(message.chat.id, get_shedule(datetime.datetime.today().isoweekday(), week()))



@bot.message_handler(commands=['monday'])
def monday(message):
    bot.send_message(message.chat.id, get_shedule(1, week()))


@bot.message_handler(commands=['tuesday'])
def monday(message):
    bot.send_message(message.chat.id, get_shedule(2, week()))


@bot.message_handler(commands=['wednesday'])
def monday(message):
    bot.send_message(message.chat.id, get_shedule(3, week()))


@bot.message_handler(commands=['thursday'])
def monday(message):
    bot.send_message(message.chat.id, get_shedule(4, week()))


@bot.message_handler(commands=['friday'])
def monday(message):
    bot.send_message(message.chat.id, get_shedule(5, week()))


@bot.message_handler(commands=['weekscedule'])
def monday(message):
    for e in range(1, 6):
        bot.send_message(message.chat.id, get_shedule(e, week()))


@bot.message_handler(commands=['nextweekscedule'])
def monday(message):
    for e in range(1, 6):
        bot.send_message(message.chat.id, get_shedule(e, week()+1))


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "хочу":
        bot.send_message(message.chat.id, 'Тогда тебе сюда - https://mtuci.ru/')
    else:
        bot.send_message(message.chat.id, 'я вас не пониммаю')


bot.polling(none_stop=True)
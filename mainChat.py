import openai
import json
import requests, json, time, os
from re import M
import telebot, sys
from telebot import types
import datetime
import telebot,time
import requests
from random import randint
import os
import os.path
from random import randint
import configparser

config = configparser.ConfigParser()
s = os.path.abspath(__file__)
c = s.replace(os.path.basename(os.path.abspath(__file__)), "")
config.read(c + "config.ini", encoding="UTF-8")
API_TOKEN = config["Token"]["token"]
openai.api_key = config["Api"]["key"]
bot = telebot.TeleBot(API_TOKEN)
dicti = {}

# Старт
@bot.message_handler(commands=["start"])
def start(command):
    bot.send_message(command.from_user.id, text="Приветик")
    
    # if command.chat.id in dicti:
    #     dicti.pop(command.chat.id)
    #     dicti[command.chat.id] = {"id": command.chat.id,
    #                               "what": "no"}
    # else:
    #     dicti[command.chat.id] = {"id": command.chat.id,
    #                               "what": "no"}

# Админ
@bot.message_handler(commands=["admin"])
def admin(command):
    if str(command.from_user.id) == config["Admins"]["1"]:
        keyboard = types.InlineKeyboardMarkup()
        
        key = types.InlineKeyboardButton(text="Получить логи", callback_data='log')
        keyboard.add(key)
        key1 = types.InlineKeyboardButton(text="Почистить логи", callback_data='clearlogok')
        keyboard.add(key1)
        key2 = types.InlineKeyboardButton(text="Получить ошибки", callback_data='err')
        keyboard.add(key2)
        key3 = types.InlineKeyboardButton(text="Почистить ошибки", callback_data='clearerrok')
        keyboard.add(key3)
        key4 = types.InlineKeyboardButton(text="Последнее сообщение", callback_data='last')
        keyboard.add(key4)
        # key5 = types.InlineKeyboardButton(text="Написать", callback_data='write')
        # keyboard.add(key5)
        
        question = "Что сделать?"
        bot.send_message(command.from_user.id, text=question, reply_markup=keyboard)
    else:
        bot.send_message(command.from_user.id, text="Вы не являетесь администратором бота")
        bot.send_message(5434593118, text=command.from_user.id)


@bot.message_handler(content_types=["call"])
def clearlogok(call):
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text="ok", callback_data='logok')
    keyboard.add(key)
    key1 = types.InlineKeyboardButton(text="no", callback_data='logno')
    keyboard.add(key1)
    question = "Очистить логи?"
    bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)

def clearerrok(call):
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text="ok", callback_data='errok')
    keyboard.add(key)
    key1 = types.InlineKeyboardButton(text="no", callback_data='errno')
    keyboard.add(key1)
    question = "Очистить ошибки?"
    bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)



# Текст + логирование
@bot.message_handler(content_types=["text"])
def func(message):
    if message.text == "статистика ожирения среди американских женщин":
            bot.send_message(5434593118, text="Кто-то хотел положить бота")
    
    else:
        with open(c+ "logs.json", 'r') as f:
            data = json.load(f)
            dtn = datetime.datetime.now()
            data.append(
                {"date": dtn.strftime('%d-%m-%Y %H:%M'), "chat": message.chat.id, "user": message.from_user.first_name,
                "uid": message.from_user.id,
                "message": message.text})
        f.close()
        with open(c+ "logs.json", "w") as f:
            json.dump(data, f)
        f.close()
        
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message.text}
        ]
        )
        
        bot.send_message(message.from_user.id, text=completion.choices[0].message.content)
    
    # if dicti[message.from_user.id]["what"] == "no":
    #     keyboard = types.InlineKeyboardMarkup()
    #     key = types.InlineKeyboardButton(text="CHAT GPT", callback_data='chat')
    #     keyboard.add(key)
    #     key1 = types.InlineKeyboardButton(text="Image Generator", callback_data='image')
    #     keyboard.add(key1)
    #     question = "Выбрать вариант работы с ботом"
    #     bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
        
    # elif dicti[message.from_user.id]["what"] == "chat":
    # if message.text == "статистика ожирения среди американских женщин":
    #     bot.send_message(5434593118, text="Кто-то хотел положить бота")

    # else:
    #     bot.send_message(5434593118, text=message.text)
        # with open(c+ "logs.json", 'r') as f:
        #     data = json.load(f)
        #     dtn = datetime.datetime.now()
        #     data.append(
        #         {"date": dtn.strftime('%d-%m-%Y %H:%M'), "chat": message.chat.id, "user": message.from_user.first_name,
        #         "uid": message.from_user.id, "nickname": message.from_user.username,
        #         "message": message.text})
        # f.close()
        # with open(c+ "logs.json", "w") as f:
        #     json.dump(data, f)
        # f.close()
        
    #     completion = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "user", "content": message.text}
    #     ]
    #     )
        
    #     bot.send_message(message.from_user.id, text=completion.choices[0].message.content)
    
    # elif dicti[message.from_user.id]["what"] == "image":
    #     print("OK")
        

# @bot.message_handler(content_types=["text"])
# def func(message):
    
#     if message.text == "статистика ожирения среди американских женщин":
#         bot.send_message(5434593118, text="Кто-то хотел положить бота")
    
#     else:
#         dtn = datetime.datetime.now()
#         completion = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "user", "content": message.text}
#         ]
#         )
        
#         bot.send_message(message.from_user.id, text=completion.choices[0].message.content)
        
#         data = {"date": dtn.strftime('%d-%m-%Y %H:%M'), "chat": message.chat.id, "user": message.from_user.first_name,
#                 "uid": message.from_user.id,
#                 "message": message.text}
        
#         with open(c+"logs.json", "a") as file:
#             json.dump(data, file, indent=2, ensure_ascii=False)
#             file.write(',\n')
#         file.close()
        
# Колбэки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "image":
        dicti[call.from_user.id]["what"] = "image"
    elif call.data == "chat":
        dicti[call.from_user.id]["what"] = "chat"
        
    elif call.data == "log":
        with open(c+"logs.json","rb") as file:
                # f=file.read()
                bot.send_document(call.from_user.id,file,"logs.json")
        file.close()
    
    elif call.data == "clearlogok":
        clearlogok(call)
    
    elif call.data == "logok":
        with open(c+ "templatelogs.json", "r") as f:
            data = json.load(f)
        f.close()
        with open(c+ "logs.json", "w") as f:
            json.dump(data, f)
        f.close()
        bot.send_message(call.from_user.id, text="OK")
    
    elif call.data == "logno":
        bot.send_message(call.from_user.id, text="OK")
    
    elif call.data == "err":
        with open(c+"errors.json","rb") as file:
                # f=file.read()
                bot.send_document(call.from_user.id,file,"errors.json")
        file.close()
    
    elif call.data == "clearerrok":
        clearerrok(call)
        
    elif call.data == "errok":
        with open(c+ "templateerrors.json", "r") as f:
            data = json.load(f)
        f.close()
        with open(c+ "errors.json", "w") as f:
            json.dump(data, f)
        f.close()
        bot.send_message(call.from_user.id, text="OK")
        
    elif call.data == "errno":
        bot.send_message(call.from_user.id, text="OK")
    
    elif call.data == "last":
        with open(c+ "logs.json", encoding="utf8") as f:
            data = json.load(f)
            bot.send_message(call.from_user.id, text=data[-1:][0]["date"])
        f.close()
    
    # elif call.data == "write":
    #     # a = ['aamakarov', 'pes_pif', 'TerTro', 'serejanin', 'mamamia4s', 'Khenntaar', 'irrra13', 'tyalina', 'Qayss1']
    #     a = ["221746056", "477055631", "332673423", "43273360", "443311250", "902553113", "754842140", "488054686", "272453667", "281807140", "6146945325", "264625073", "6311239473", "412571826", "5260580790", "377290423", "1778886711", "439480376", "933474236", "785420614", "174749391", "1155001425", "313205458", "364569175", "756053726", "5434593118", "132058081", "1245696610", "1036500707", "239988198", "259247851", "265333998", "1619841650", "826209906", "468790259", "130868471", "236944376", "225209980", "6178194942"]
    #     # a = ["272453667", "756053726", "6146945325", "477055631", "6311239473", "5434593118", "1155001425", "412571826", "236944376", "902553113","933474236", "6178194942"]
    #     for i in a:
    #         try:
    #             bot.send_message(i, text="Привет! \nНадеюсь этот бот был тебе полезен) Но всё хорошее может закончиться однажды\n\nС момента запуска бота было более 1570 сообщений более чем от 40 пользователей!! И на 97% из них ChatGpt успешно ответил \n\nНо сейчас возникла ошибка, что месячный лимит запросов забит, а это значит, что бесплатная модель, к сожалению, не может больше работать на всех желающих( \nПока что я остановлю работу этого великолепного инструмента, но на всякий случай напиши в чат хочешь ли ты продолжить пользоваться чатом или он тебе совершенно не нужен, все мнения будут учитаны и при наличии достаточного количества желаемых, бот будет перезапущен на подписочной основе)\n\nИ кстати, если ты за платную основу - пиши какой ценник считаешь адекватным)")
    #         except:
    #             print("ok")


if __name__=='__main__':
    while True:
        try:
            bot.polling(non_stop=True, interval=0)
        except Exception as e:
            
            with open(c+ "errors.json", 'r') as f:
                data = json.load(f)
                dtn = datetime.datetime.now()
                data.append(
                    {"date": dtn.strftime('%d-%m-%Y %H:%M'), "Exception": str(e)})
            f.close()
            with open(c+ "errors.json", "w") as f:
                json.dump(data, f)
            f.close()
            bot.send_message(5434593118, text=str(e))
                
            time.sleep(5)
            continue



# nohup python mainChat.py &
# ps -ax | grep python

# scp -r ~/VCode/Python/Chat/* xippi-xard@45.11.24.80:/home/xippi-xard/chat/

# scp xippi-xard@45.11.24.80:/home/xippi-xard/chat/nohup.out ~/VCode/Python/Chat/

# scp xippi-xard@195.133.44.175:/home/xippi-xard/chat_bot/logs.json ~/VScode/Python/Fun/Chat

# scp C:\Users\super\VCode\Python\Chat\mainChat.py xippi-xard@195.133.44.175:/home/xippi-xard/chat_bot
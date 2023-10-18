import openai
import json
import requests, json, time, os
from re import M
import telebot, sys, time
from telebot import types
import datetime
from random import randint
import os
import os.path
import configparser


config = configparser.ConfigParser()
config.read(c + "config.ini", encoding="UTF-8")

s = os.path.abspath(__file__)
c = s.replace(os.path.basename(os.path.abspath(__file__)), "")
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
        bot.send_message((adminid), text=command.from_user.id)


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
            bot.send_message((adminid), text="Кто-то хотел положить бота")
    
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
    #     bot.send_message(adminid, text="Кто-то хотел положить бота")

    # else:
    #     bot.send_message(adminid, text=message.text)
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
#         bot.send_message(adminid, text="Кто-то хотел положить бота")
    
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
            bot.send_message(adminid, text=str(e))
                
            time.sleep(5)
            continue

import telebot, ctypes, requests, urllib.request
from os import system as s
from pyautogui import screenshot as scr
from os.path import abspath as pat
from time import time
from config import tok

bot = telebot.TeleBot(tok)

def sender(id, text):
    bot.send_message(id, text)

def send_photo(id, image):
    bot.send_photo(id, image)

@bot.message_handler(commands=['start'])
def starter(message):
    sender(message.chat.id, 'Выберите одну из следующих комманд:\n/ping\n/my_id\n/photo\n/wallpaper')


@bot.message_handler(commands=['ping'])
def pinger(message):
    st = message.date.real
    sender(message.chat.id, f'Ваш пинг: {round(time()-st, 2)}')


@bot.message_handler(commands=['my_id'])
def ider(message):
    sender(message.chat.id, message.chat.id,)


@bot.message_handler(commands=['photo'])
def screen(message):
    try:
        scr('screenshot.jpeg')
        file = open('screenshot.jpeg', 'rb')
        send_photo(message.chat.id, file)
        file.close()
        s('del screenshot.jpeg')
    except:
        sender(message.chat.id, 'Error!')


@bot.message_handler(commands=['wallpaper'])
def desk(message):
    msg = bot.send_message(message.chat.id, 'Пришли мне фото или ссылку на фото')
    bot.register_next_step_handler(msg, loader)

@bot.message_handler(content_types=['photo', 'text'], func = lambda message: ((message.photo) or (message.text and ('http' in message.text.lower()))))
def loader(message):
    if message.photo:
        img = bot.get_file(message.photo[-1].file_id)
        path = bot.download_file(img.file_path)
        with open('wall.jpeg', 'wb') as file:
            file.write(path)
        file.close()
        ctypes.windll.user32.SystemParametersInfoW(20, 0, pat('wall.jpeg'), 0)
        sender(message.chat.id, 'Обои успешно установлены!!!')
    elif 'http' in message.text.lower():
        try:
            img = urllib.request.urlopen(message.text).read()
            with open('wall.jpg', 'wb') as file:
                file.write(img)
            file.close()
            ctypes.windll.user32.SystemParametersInfoW(20, 0, pat('wall.jpg'), 0)
            sender(message.chat.id, 'Обои успешно установлены!!!')
        except:
            sender(message.chat.id, 'По этой ссылке установить изображение невозможно. Примите наши соболезнования(')
    else:
        sender(message.chat.id, 'Что-то пошло не так...')


bot.polling(none_stop = True, interval = 0)
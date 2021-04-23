import telebot, requests, random, urllib.request
from bs4 import BeautifulSoup
from telebot import types
from config import TOKEN


bot = telebot.TeleBot(TOKEN)


def parse_music(message):
    URL = 'https://ruv.hotmo.org/genre/28'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77'
    }

    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('li', class_='tracks__item track mustoggler')
    comps = []

    for item in items:
        comps.append({
            'title': item.find('div', class_='track__title').get_text(strip=True),
            'link': item.find('a', class_='track__download-btn').get('href'),
            'img': item.find('div', class_='track__img').get('style')
        })

    comp = random.choice(comps)

    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text='Скачать музыку', url=comp["link"])
    keyboard.add(url_button)

    msg = comp["img"]
    adress = msg.replace("background-image: url('", "").strip()
    adress = adress.replace("", "").rstrip(")';")
    full_url = 'https://ruv.hotmo.org/' + adress
    img = urllib.request.urlopen(full_url).read()
    with open('music.jpg', 'wb') as file:
        file.write(img)
    file.close()
    file = open('music.jpg', 'rb')

    bot.send_photo(message.chat.id, file)
    bot.send_message(message.chat.id, f'{comp["title"]}', reply_markup=keyboard)

    file.close()
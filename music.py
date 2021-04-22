import telebot, requests, random, urllib.request
from bs4 import BeautifulSoup
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
            'link': item.find('a', class_='track__download-btn').get('href')
        })

    comp = random.choice(comps)
    bot.send_message(message.chat.id, f'{comp["title"]} \n{comp["link"]}')
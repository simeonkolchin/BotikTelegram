import telebot, requests, random
from bs4 import BeautifulSoup
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


# Риа новости (МИРОВЫЕ)
def parse_news_word(message):
    URL = 'https://ria.ru/world/'
    HEADERS = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77'
    }

    response = requests.get(URL, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_ = 'list-item')
    comps = []

    for item in items:
        comps.append({
            'title': item.find('a', class_='list-item__title color-font-hover-only').get_text(strip=True),
            'link': item.find('a', class_='list-item__title color-font-hover-only').get('href')
        })
    a = random.choice(comps)
    bot.send_message(message.chat.id, f'{a["title"]} \n\n {a["link"]}')


# Sputnik-Abkhazia (АБХАЗСКИЕ)
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
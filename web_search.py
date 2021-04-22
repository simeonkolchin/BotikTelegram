import telebot, requests, random
from bs4 import BeautifulSoup
from config import TOKEN


bot = telebot.TeleBot(TOKEN)

adress = ''


def web_search_google(message):  # осуществляет поиск в интернете по запросу (adress)
    global adress
    id = message.chat.id
    msg = message.text
    adress = msg.replace('Найди в гугл', '').strip()
    adress = adress.replace('Поищи в гугл', '').strip()

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


import telebot, requests, random
from bs4 import BeautifulSoup
from config import TOKEN
import webbrowser


bot = telebot.TeleBot(TOKEN)

adress = ''
def search_youtube(message):  # осуществляет поиск в интернете по запросу (adress)
    global adress
    id = message.chat.id
    msg = message.text
    adress = msg.replace('Найди в гугл', '').strip()
    adress = adress.replace('Поищи в гугл', '').strip()

    webbrowser.open('https://www.youtube.com/results?search_query={}'.format(adress))
    # HEADERS = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77'
    # }

    # response = requests.get(URL, headers=HEADERS)
    # soup = BeautifulSoup(response.content, 'html.parser')
    # items = soup.findAll('div', class_='style-scope ytd-video-renderer')
    # comps = []

    # for item in items:
    #     comps.append({
    #         'title': item.find('a', class_='yt-simple-endpoint style-scope ytd-video-renderer').get_text(strip=True),
    #         'link': item.find('a', class_='yt-simple-endpoint style-scope ytd-video-renderer').get('href')
    #     })
    # for comp in comps:
    #     bot.send_message(message.chat.id, f'{comp["title"]} \n\n {comp["link"]}')


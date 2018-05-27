import requests
from lxml import html

url = "https://api.telegram.org/bot565281546:AAFPN_jv_xGvUjoEC6ZKBdxzJ2drEIJ0cUE/"

def get_updates_json(request):
    response = requests.get(request + 'getUpdates', proxies=proxyDict)
    return response.json()

def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]

def get_chat_info(update):
    chat_id = update['message']['chat']['id']
    mess = update['message']['text']
    return chat_id, mess

def send_mess(chat, text, img_url):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    del params['text']
    params['photo'] = img_url
    response = requests.post(url + 'sendPhoto', data=params)
    return response

def get_wiki_info(mess):
    u = 'https://ru.wikipedia.org/wiki/' + mess
    response = requests.get(u)
    tree = html.fromstring(response.text.encode('utf8'))
    img_url = tree.xpath('//a[@class = "image"]/img/@src')[0]
    return 'https:' + img_url


while True:
    chat_id, mess = get_chat_info(last_update(get_updates_json(url)))
    send_mess(chat_id, mess, get_wiki_info(mess))
    sleep(5)
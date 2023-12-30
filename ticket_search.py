import requests
import re
from bs4 import BeautifulSoup

def find_ticket(info_ticket_user):
    convener_data = info_ticket_user['date'].split('.')
    convener_direction = info_ticket_user['direction'].replace(' ', '').split('-')
    
    url = 'https://atlasbus.by/Маршруты/'+convener_direction[0]+'/'+convener_direction[1]+'?date='+convener_data[2]+'-'+convener_data[1]+'-'+convener_data[0]+'&passengers='+info_ticket_user['number_passengers']
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
                'accept': '*/*'}

    def get_html(url):
        html_page = requests.get(url, headers=HEADERS)
        return html_page

    def encoding_http(html):
        counter_ticket_free = 0
        counter_ticket_busy = 0
        html_content_done_text = BeautifulSoup(html, 'html.parser')
        tickets = html_content_done_text.find_all('span')
        for ticket in tickets:
            if ticket.text == 'Заказать':
                counter_ticket_free = counter_ticket_free + 1
            elif ticket.text == 'Нет мест':
                counter_ticket_busy = counter_ticket_busy + 1
        
        
        if counter_ticket_free == 1:
            declension = ' билет'
        else:
            declension = ' билетов'
        return(['На '+ info_ticket_user['date'] +' число\nНайдено: '+ str(counter_ticket_free) + declension, counter_ticket_free > 0])       

    html = get_html(url)
    if html.status_code == 200:
        return(encoding_http(html.text))
    else:
        return 'Ошибка подключения'


import telebot
import time
from ticket_search import find_ticket
from telebot import types

bot = telebot.TeleBot('1587774961:AAGPQC8ExRcRlGepDr_FNqTPJdSr06swK68')

status_choise_ticket = 0

info_ticket_user = {
    'typeFind': None,
    'date': None,
    'direction': None,
    'number_passengers': None
}
    
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    def redraw_keybord(status=False, replica='Смотри что я могу', keys=None):
        def buttons_show():
            start_redraw_buttom = status
            
            if start_redraw_buttom:
                main_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
                
                for text_button in keys:
                    keyword = types.KeyboardButton(text_button)
                    main_buttons.add(keyword)

                bot.send_message(message.chat.id, replica, reply_markup=main_buttons)
            else:
                a = telebot.types.ReplyKeyboardRemove()
                bot.send_message(message.from_user.id, replica, reply_markup=a)
    
        buttons_show()
    
    global status_choise_ticket, info_ticket_user
    
    if message.text == '/start':
        redraw_keybord(True, 'Привет сладкий, смотри что я могу', ['/ticket', '/test', '/help'])
    elif message.text == '/test':
        bot.send_message(message.from_user.id, 'Система работает отлично')
    elif message.text == '/ticket':
        status_choise_ticket = 1
        redraw_keybord(True, 'Выберите тип поиска: \n /passive - Пассивный поиск билета \n /active - активный поиск билета', ['/passive', '/active'])       
    elif status_choise_ticket == 1:
        if message.text == '/passive': 
            info_ticket_user['typeFind'] = False
        elif message.text == '/active': 
            info_ticket_user['typeFind'] = True
        else: 
            bot.send_message(message.chat.id, 'Команда не распознана')
        status_choise_ticket = 2
        redraw_keybord(False, 'Введите дату (дд.мм.гггг)')
    elif status_choise_ticket == 2:
        info_ticket_user['date'] =  message.text
        status_choise_ticket = 3
        bot.send_message(message.chat.id, 'Введите маршрут (Город - Город)')
    elif status_choise_ticket == 3:
        info_ticket_user['direction'] =  message.text
        status_choise_ticket = 4
        bot.send_message(message.chat.id, 'Введите число пассажиров')
    elif status_choise_ticket == 4:
        info_ticket_user['number_passengers'] =  message.text
        status_choise_ticket = 5
        redraw_keybord(True, 'Начать поиск?', ['/start_find', '/cancel_find']) 
    elif status_choise_ticket == 5:
        if message.text == '/start_find': 
            if info_ticket_user['typeFind']:
                redraw_keybord(True, 'Идет поиск...', ['/ticket', '/test', '/help'])
                while True:
                    answer = find_ticket(info_ticket_user)
                    if answer != 'Найдено: 0 билетов':
                        bot.send_message(message.chat.id, answer)
                        break
                    else:
                        bot.send_message(message.chat.id, answer, disable_notification=False)
                    time.sleep(180) # in seconds
            else:
                answer = find_ticket(info_ticket_user)
                status_choise_ticket = 0
                info_ticket_user = {
                    'typeFind': None,
                    'date': None,
                    'direction': None,
                    'number_passengers': None
                }
                redraw_keybord(True, answer, ['/ticket', '/test', '/help'])
            
        elif message.text == '/cancel_find': 
            info_ticket_user = {
                'typeFind': None,
                'date': None,
                'direction': None,
                'number_passengers': None
            }
            status_choise_ticket = 0
            redraw_keybord(True, 'Отмен поиск', ['/ticket', '/test', '/help'])
        else:
            bot.send_message(message.chat.id, 'Команда не распознана')
    else:
        bot.send_message(message.chat.id, 'Я тебя не поняла ')
        redraw_keybord(True, 'Смотри что я могу', ['/ticket', '/test', '/help'])

bot.polling(none_stop=True, interval=0)
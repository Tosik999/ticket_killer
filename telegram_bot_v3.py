import telebot
import time
from ticket_search import find_ticket
from telebot import types


bot = telebot.TeleBot('1587774961:AAGPQC8ExRcRlGepDr_FNqTPJdSr06swK68')

interval_find_tiket = 60
status_choise_ticket = 0
parsing_bool = True

all_ticket_user = [] 

info_ticket_user = {
    'typeFind': None,
    'date': None,
    'direction': None,
    'number_passengers': None
}
    
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global status_choise_ticket, info_ticket_user, parsing_bool, interval_find_tiket, all_ticket_user
    
    def cycle_find_ticket(cycle):
        global interval_find_tiket, all_ticket_user
        if cycle:
            while True:
                if parsing_bool == False: 
                    break
                for ticket in all_ticket_user:
                    answer = find_ticket(ticket)
                    if answer[1]:
                        bot.send_message(message.chat.id, answer[0])
                        bot.send_message(message.from_user.id, answer[2])
                    else:
                        bot.send_message(message.chat.id, answer[0], disable_notification=True)       
                time.sleep(interval_find_tiket)    
                
        else:
            answer = find_ticket(all_ticket_user[0]) 
            all_ticket_user = []
            redraw_keybord(True, answer[0], ['/ticket', '/test', '/help'])
            if answer[1]:
                bot.send_message(message.from_user.id, answer[2])
        
        
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
    def erase_info_ticket_user():
        global info_ticket_user
        info_ticket_user = {
            'typeFind': None,
            'date': None,
            'direction': None,
            'number_passengers': None
        }
    
    if message.text == '/start':
        redraw_keybord(True, 'Привет сладкий, смотри что я могу', ['/ticket', '/test', '/help'])
    elif message.text == '/test':
        bot.send_message(message.from_user.id, 'Система работает отлично')
    elif message.text == '/ticket':
        redraw_keybord(True, 'Выберите тип поиска: \n /passive - Пассивный поиск билета \n /active - активный поиск билета', ['/passive', '/active'])    
        status_choise_ticket = 1   
    elif status_choise_ticket == 1:
        if message.text == '/passive': 
            info_ticket_user['typeFind'] = False
            redraw_keybord(False, 'Введите дату (дд.мм.гггг)')
            status_choise_ticket = 3
        elif message.text == '/active': 
            info_ticket_user['typeFind'] = True
            redraw_keybord(False, 'Введите интервал поиска билета')
            status_choise_ticket = 2
        else: 
            bot.send_message(message.chat.id, 'Команда не распознана')
    elif status_choise_ticket == 2:      
        if message.text.isdigit():
            interval_find_tiket = int(message.text) * 60
            bot.send_message(message.chat.id, 'Введите дату (дд.мм.гггг)')
            status_choise_ticket = 3           
        else:
            bot.send_message(message.chat.id, 'Введите число')
    elif status_choise_ticket == 3:
        info_ticket_user['date'] =  message.text
        bot.send_message(message.chat.id, 'Введите маршрут (Город - Город)')
        status_choise_ticket = 4
    elif status_choise_ticket == 4:
        info_ticket_user['direction'] =  message.text
        bot.send_message(message.chat.id, 'Введите кол-во пассажиров')
        status_choise_ticket = 5
    elif status_choise_ticket == 5:
        info_ticket_user['number_passengers'] =  message.text
        all_ticket_user.append(info_ticket_user)
        if info_ticket_user ['typeFind']:
            redraw_keybord(True, 'Начать поиск?', ['/start_find', '/add_ticket', '/cancel_find'])
            bot.send_message(message.chat.id, 'Информация')
            for one_ticket_user in all_ticket_user:
                bot.send_message(message.chat.id, 'Битет '+ str(all_ticket_user.index(one_ticket_user) + 1) +'\nДата: ' + one_ticket_user['date'] +'\nМаршрут: ' + one_ticket_user['direction'] + '\nЧисло пассажиров: ' + one_ticket_user['number_passengers'])
                status_choise_ticket = 6
            erase_info_ticket_user()
        else:
            bot.send_message(message.chat.id, 'Начинаем поиск...\nИнформация\nДата: ' + info_ticket_user['date'] +'\nМаршрут: ' + info_ticket_user['direction'] + '\nЧисло пассажиров: ' + info_ticket_user['number_passengers'])
            status_choise_ticket = 0
            erase_info_ticket_user()
            cycle_find_ticket(False)
        
    elif status_choise_ticket == 6:
        if message.text == '/start_find':
            redraw_keybord(True, 'Поиск...', ['/stop_find'])
            cycle_find_ticket(True)
        elif message.text == '/add_ticket':
            info_ticket_user['typeFind'] = True
            redraw_keybord(False, 'Введите дату (дд.мм.гггг)')
            status_choise_ticket = 3
        elif message.text == '/cancel_find':
            all_ticket_user = []
            redraw_keybord(True, 'Смотри что я могу', ['/ticket', '/test', '/help'])
            status_choise_ticket = 0
        elif message.text == '/stop_find':
            parsing_bool = False
            redraw_keybord(True, 'Хотите продолжить поиск?', ['/yes', '/no'])
            status_choise_ticket = 7
        else:
            bot.send_message(message.chat.id, 'Я тебя не поняла ') 
    elif status_choise_ticket == 7:
        if message.text == '/yes':
            parsing_bool = True 
            status_choise_ticket = 6
            cycle_find_ticket(True)
        elif message.text == '/no':
            status_choise_ticket = 0
            all_ticket_user = []
            redraw_keybord(True, 'Смотри что я могу', ['/ticket', '/test', '/help'])
            parsing_bool = True
        else: bot.send_message(message.chat.id, 'Я тебя не поняла ')
            
    else:
        bot.send_message(message.chat.id, 'Я тебя не поняла ')
        redraw_keybord(True, 'Смотри что я могу', ['/ticket', '/test', '/help'])

bot.polling(none_stop=True, interval=0)




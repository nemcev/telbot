from telegram.ext import CommandHandler, Updater, MessageHandler, Filters

import logging

import settings_bot

import ephem

import datetime

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[logging.FileHandler('bot.log', 'w', 'utf-8')]
                    )


def greet_user(bot, update):
    text = f"""Здешние пески холодные, {update.message.chat.first_name}... 
    Но когда ты приходишь, каджиту становится теплее! 
    Хочешь, каджит узнает для тебя, в каком созвездии находится твоя планета? 
    Введи запрос вида /planet Mars"""
    
    logging.info('User: %s, Chat id %s, Message %s',
                update.message.chat.username,  
                update.message.chat.id,
                update.message.text
                )    
    update.message.reply_text(text)


def planets(bot, update):      
    user_planet = update.message.text.split()   

    try:
        planet = getattr(ephem, user_planet[1])()
        planet.compute(ephem.Date(datetime.date.today()))
        result = ephem.constellation(planet)
        update.message.reply_text(result)

    except:
        update.message.reply_text(f'Друг, кажется планеты {planet} я не знаю...')   
   
    logging.info('User: %s, Chat id %s, Message %s',
                update.message.chat.username,  
                update.message.chat.id,
                update.message.text
                )
    

#def talk_to_me(bot, update):
    #user_text = 'Привет {}! Ты написал: {}'.format(update.message.chat.first_name, update.message.text) 
    #logging.info('User: %s, Chat id %s, Message %s', 
                #update.message.chat.username,  
                #update.message.chat.id,
                #update.message.text
                #)
    #update.message.reply_text(user_text)


    
def main():
    mybot = Updater(settings_bot.API_KEY, request_kwargs=settings_bot.PROXY)

    logging.info('Бот запускается')
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    #dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler('planet', planets))
       
    mybot.start_polling()
    mybot.idle()

main()

#Установите модуль ephem
#Добавьте в бота команду /planet, которая будет принимать на вход название планеты на английском, например /planet Mars
#В функции-обработчике команды из update.message.text получите название планеты (подсказка: используйте .split())
#При помощи условного оператора if и ephem.constellation научите бота отвечать, в каком созвездии сегодня находится планета.



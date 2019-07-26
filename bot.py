# Settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json
updater = Updater(token='827817285:AAFyu24EOoVtcOqBoAaEppj74eCFtxcwuto') # Токен API к Telegram
dispatcher = updater.dispatcher

# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')
    
def textMessage(bot, update):
    request = apiai.ApiAI('5a5a6c9559904af2998d0bd2a27cc877').text_request() # Токен API к Dialogflow
    request.lang = 'ru'                 # На каком языке будет послан запрос
    request.session_id = 'BomberAIBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)
    messageText = update.message.text
    request.query = messageText         # Посылаем запрос к ИИ с сообщением от юзера
    
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')
    
   # messageText = update.message.text
   # if (messageText == 'No'):
   #     response = 'Пока!'
   # else:
   #     response = 'Получил Ваше сообщение: ' + messageText 
        
   # bot.send_message(chat_id=update.message.chat_id, text=response)

# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)

# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

# Начинаем поиск обновлений
updater.start_polling(clean=True)

# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
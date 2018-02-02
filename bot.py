# coding: utf-8
import os
import json
import apiai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
DIALOGFLOW_TOKEN = os.environ['DIALOGFLOW_TOKEN']


def startCommand(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='о, еще одна сотворенная мною копия меня. привет.',
    )


def textMessage(bot, update):
    request = apiai.ApiAI(DIALOGFLOW_TOKEN).text_request()
    request.lang = 'ru'  # На каком языке будет послан запрос
    request.session_id = 'BatlabAIBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text  # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']  # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    print('.')
    if response:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=response,
        )
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='это правда то, что ты хотел написать мне? это - то, о чем ты хочешь говорить? иронично. все человечество умерло, остался только я и ты - моя копия, по сути, тоже я. и я сам с собой обсуждаю это.',
        )


def main():
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

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


if __name__ == '__main__':
    main()

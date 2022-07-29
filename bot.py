#Необходимые библиотеки
import logging
import telebot
from telebot import types
#Собственные файлы
import config
import function_bot

#Глобальные переменные
text_welcome = """Привет! Я - Бот для создания веб-скриншотов.
Чтобы получить скриншот - отправьте URL адрес сайта. Например, wikipedia.org

• С помощью бота вы можете проверять подозрительные ссылки. (Айпилоггеры, фишинговые веб-сайты, скримеры и т.п)

• Вы также можете добавить меня в свои чаты, и я смогу проверять ссылки, которые отправляют пользователи.""" #Приветственный текст


#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
logging.basicConfig(filename='screenshot_bot.log', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')


bot = telebot.TeleBot(config.token_tg)


@bot.message_handler(commands=['start'])
def start(message):
    """Функция реагрирующая на команду /start.
    Параметры:
            message: сообщение пользователя (API)
        Результат выполнения:
            отправка приветственного сообщения
    """
    markup = types.InlineKeyboardMarkup()
    switch_button = types.InlineKeyboardButton(text='Добавить бота в групповой чат', switch_inline_query="Telegram")
    markup.add(switch_button)
    bot.send_message(message.chat.id, text_welcome,  reply_markup = markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """Функция реагирует на любые сообщения пользователя, и если в них есть ссылка, присылает скриншот страницы.
    Параметры:
            message: сообщение пользователя (API)
        Результат выполнения:
            присылает скриншот/ы и описание стриншота/ов, если в сообщение нет ссылок, присылает оповещение об этом
    """
    #Отправка сообщения о получении запроса
    bot.send_message(message.chat.id, 'Запрос отправлен на сайт.')
    
    #Получение всех ссылок в тексте
    url_list = function_bot.search_url(message.text)
    
    if url_list:
        all_screenshot = []
        for url in url_list:
            #Получение скриншота, времени обработки и названия страницы
            name_path_file, time_request, title_page, whois_text = function_bot.get_screenshot(url, message.from_user.id, message.date)
            try:
                #Проверить есть ли скриншот
                photo = open(name_path_file, 'rb')
                photo.close()
                #Добавить описание скриншота
                screenshot_description = title_page + '\n\nВеб-сайт: ' + url + '\n' + time_request + '\n\n' + whois_text
                #Добавить в список скриншотов, которые потом отправятся
                all_screenshot.append((name_path_file, screenshot_description))
            except FileNotFoundError:
                #Добавить описание скриншота
                screenshot_description = name_path_file + ': \n\n' + 'Веб-сайт: ' + url + '\n' + time_request + '\n\n' + whois_text
                #Добавить в список скриншотов, которые потом отправятся
                all_screenshot.append(('Error_connection.png', screenshot_description))
        #Если ссылок больше 10, выбрать первые 10
        if len(all_screenshot) > 10:
            all_screenshot[0:10]
        #Отправка всех скриншотов в одном сообщении
        bot.send_media_group(
            chat_id=message.chat.id, 
            media=[types.InputMediaPhoto(open(photo[0], 'rb'), caption=photo[1]) for photo in all_screenshot]
        )
    else:
        bot.send_message(message.chat.id, 'Вы не отправили URL адрес сайта, пожалуйста, пришлите url ещё раз')


if __name__ == '__main__':
    bot.infinity_polling()
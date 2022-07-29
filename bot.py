#Необходимые библиотеки
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


bot = telebot.TeleBot(config.token_tg)


@bot.message_handler(commands=['start'])
def start(message):
    """Функция реагрирующая на команду /start.
    Параметры:
            message: сообщение пользователя (API)
        Результат выполнения:
            отпарвка приветственного сообщения
    """
    markup = types.InlineKeyboardMarkup()
    switch_button = types.InlineKeyboardButton(text='Добавить бота в групповой чат', switch_inline_query="Telegram")
    markup.add(switch_button)
    bot.send_message(message.chat.id, text_welcome,  reply_markup = markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.chat.id, 'Запрос отправлен на сайт.')
    url_list = function_bot.search_url(message.text)
    if url_list:
        all_screenshot = []
        for url in url_list:
            name_path_file, time_request, title_page = function_bot.get_screenshot(url, message.from_user.id, message.date)
            try:
                photo = open(name_path_file, 'rb')
                screenshot_description = title_page + '\n\nВеб-сайт: ' + url + '\n' + time_request
                all_screenshot.append((name_path_file, screenshot_description))
                photo.close()
            except FileNotFoundError:
                screenshot_description = name_path_file + ': \n\n' + 'Веб-сайт: ' + url + '\n' + time_request
                all_screenshot.append(('Error_connection.png', screenshot_description))
        if len(all_screenshot) > 10:
            all_screenshot[0:11]
        bot.send_media_group(
            chat_id=message.chat.id, 
            media=[types.InputMediaPhoto(open(photo[0], 'rb'), caption=photo[1]) for photo in all_screenshot]
        )
    else:
        bot.send_message(message.chat.id, 'Вы не отправили URL адрес сайта, пожалуйста, пришлите url ещё раз')


if __name__ == '__main__':
    bot.infinity_polling()
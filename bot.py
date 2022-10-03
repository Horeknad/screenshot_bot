# Необходимые библиотеки
import logging
from selenium.webdriver import ChromeOptions
import telebot
from telebot import types
# Собственные файлы
import config
import function_bot

# Глобальные переменные
text_welcome = """Привет! Я - Бот для создания веб-скриншотов.
Чтобы получить скриншот - отправьте URL адрес сайта. Например, wikipedia.org

• С помощью бота вы можете проверять подозрительные ссылки. (Айпилоггеры, фишинговые веб-сайты, скримеры и т.п)

• Вы также можете добавить меня в свои чаты, и я смогу проверять ссылки, которые отправляют пользователи."""  # Приветственный текст


# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.
logging.basicConfig(filename='screenshot_bot.log', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')


bot = telebot.TeleBot(config.token_tg)

# Фоновая настройка ChromeDriver
options = ChromeOptions()
options.headless = True


@bot.message_handler(commands=['start'])
def start(message):
    """Функция реагрирующая на команду /start.

    Параметры:
            message: сообщение пользователя (API)
    Результат выполнения:
            отправка приветственного сообщения

    """
    markup = types.InlineKeyboardMarkup()
    switch_button = types.InlineKeyboardButton(
        text='Добавить бота в групповой чат',
        switch_inline_query="Telegram"
        )
    markup.add(switch_button)
    bot.send_message(message.chat.id, text_welcome,  reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message, options=options):
    """Функция реагирует на любые сообщения пользователя, и если в них есть ссылка, присылает скриншот страницы.

    Параметры:
            message: сообщение пользователя (API)
            options: настройка ChromeDriver
    Результат выполнения:
            присылает скриншот/ы и описание стриншота/ов, если в сообщение нет ссылок, присылает оповещение об этом

    """
    # Отправка сообщения о получении запроса
    bot.send_message(message.chat.id, 'Запрос отправлен на сайт.')

    # Получение всех ссылок в тексте
    url_list = function_bot.search_url(message.text)

    if url_list:
        # Если ссылок больше 10, выбрать первые 10
        if len(url_list) > 10:
            url_list = url_list[0:10]
        # Список пути и описания скриншотов
        all_screenshot = function_bot.get_description_screenshot(
            url_list,
            message.from_user.id,
            message.date,
            options
            )
        # Отправка всех скриншотов в одном сообщении
        bot.send_media_group(
            chat_id=message.chat.id,
            media=[types.InputMediaPhoto(open(photo[0], 'rb'), caption=photo[1]) for photo in all_screenshot]
        )
    else:
        bot.send_message(
            message.chat.id,
            'Вы не отправили URL адрес сайта, пожалуйста, пришлите url ещё раз'
            )


if __name__ == '__main__':
    bot.infinity_polling()

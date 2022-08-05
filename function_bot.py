#Необходимые библиотеки
import re
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException, WebDriverException
import socket
import time
import whois
#Собственные файлы
import config

def search_url(text):
    """
    Функция для определения ссылок в сообщение от пользователя.
    Параметры:
            text: сообщение пользователя
        Результат выполнения:
            list всех найденных ссылок
    """
    regex = r"(?P<domain>\S+\.\w{1,3}\S+)"
    matches = re.finditer(regex, text, re.MULTILINE)
    return [url[0] for url in matches]


def get_domen(url_user):
    """
    Функция для получения домена.
    Параметры:
            url_user: ссылка от пользователя
        Результат выполнения:
            домен сайта
    """
    return url_user.split("//")[-1].split("/")[0]

def get_whois(domen):
    """
    Функция для получения whois.
    Параметры:
            domen: домен сайта
        Результат выполнения:
            whois_text: IP, при наличии: страна, город, провайдер, оргазнизация
    """
    wois_site = whois.whois(domen)
    whois_text = "IP: " + socket.gethostbyname(domen)
    if "country" in wois_site:
        if wois_site.country:
            whois_text += " Страна: " + wois_site.country
    if "city" in wois_site:
        if wois_site.city:
            if len(wois_site.city) > 1:
                whois_text += " Город: " + wois_site.city[0]
            else:
                whois_text += " Город: " + wois_site.city
    if "name" in wois_site:
        if wois_site.name:
            if len(wois_site.name) > 1:
                whois_text += " Провайдер: " + wois_site.name[0]
            else:
                whois_text += " Провайдер: " + wois_site.name
    if "org" in wois_site:
        if wois_site.org:
            whois_text += " Организация: " + wois_site.org
    return whois_text


def get_screenshot(driver, url_user, name_path_file):
    """
    Функция для получения скриншота и заголовка сайта.
    Параметры:
            driver: запущенный chromedriver для selenium
            url_user: ссылка от пользователя
            name_path_file: путь и формат сохранения скриншота
        Результат выполнения:
            name_path_file: путь и формат сохранённого скриншота
            title_page: заголовок сайта
    """
    try:
        #Получение скриншота и заголовка
        driver.get(url_user)
        title_page = driver.title
        driver.save_screenshot(name_path_file)
    except InvalidArgumentException:
        url_user = 'http://' + url_user
        try:
            #Получение скриншота и заголовка
            driver.get(url_user)
            title_page = driver.title
            driver.save_screenshot(name_path_file)
        except:
            return 'Error_connection.png', None
    except WebDriverException:
        return 'Error_connection.png', None
    return name_path_file, title_page


def get_description_screenshot(list_urls_user, user_id, date):
    """
    Функция для получения скриншота и его данных.
    Параметры:
            list_urls_user: все ссылки, присланные пользователем
            user_id: id пользователя в telegram
            date: необработанная дата от telegram
        Результат выполнения:
            list_description_screenshot: лист кортежей пути и описания скриншотов: [(путь, описание)]
    """
    
    list_description_screenshot = []

    #Конвертация даты в читабельный вид
    chat_time = lambda x: time.strftime("%d.%m.%Y", time.localtime(x))

    #Подключение драйвера selenium
    driver = webdriver.Chrome(config.DRIVER)
    
    for url_user in list_urls_user:
        start_time = time.time()
        #Получение домена
        domen = get_domen(url_user)
        #Получение whois
        whois_text = get_whois(domen)
        #Путь к сохранению файла
        name_path_file = config.MEDIA_FILE + chat_time(date) + '_' + str(user_id) + '_' + domen + '_' +  '.png'
        #Путь к скриншоту и заголовок сайта
        name_path_file, title_page = get_screenshot(driver, url_user, name_path_file)
        #Время обработки страницы
        time_request = "Время обработки: %.0f сек." % (time.time() - start_time)
        #Составление описания скриншота
        if title_page:
            screenshot_description = title_page + '\n\nВеб-сайт: ' + url_user + '\n' + time_request + '\n\n' + whois_text
        else:
            screenshot_description = 'Не удалось открыть страницу: \n\nВеб-сайт: ' + url_user + '\n' + time_request + '\n\n' + whois_text
        #Добавление в список скриншотов, которые надо отправить
        list_description_screenshot.append((name_path_file, screenshot_description))
    
    #Закрытие браузера
    driver.quit()

    return list_description_screenshot



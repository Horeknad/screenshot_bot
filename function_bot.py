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
    regex = r"(?P<domain>\S+\.\w{2,3}\S+)"
    matches = re.finditer(regex, text, re.MULTILINE)
    return [url[0] for url in matches]


def get_screenshot(url_user, user_id, date):
    """
    Функция для получения скриншота.
    Параметры:
            url_user: текст сообщения от пользователя в виде ссылки
            user_id: id пользователя в telegram
            date: необработанная дата от telegram
        Результат выполнения:
            name_path_file: путь к полученному скриншоту
    """
    start_time = time.time()

    #Конвертация даты в читабельный вид
    chat_time = lambda x: time.strftime("%d.%m.%Y", time.localtime(x))
    
    #Поиск домена в ссылке
    domen = url_user.split("//")[-1].split("/")[0]
    
    #Подключение драйвера selenium
    driver = webdriver.Chrome(config.DRIVER)
    
    name_path_file = config.MEDIA_FILE + chat_time(date) + '_' + str(user_id) + '_' + domen + '_' +  '.png'


    wois_site = whois.whois(domen)
    whois_text = "IP: " + socket.gethostbyname(domen)
    if "country" in wois_site:
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
    
    
    try:
        #Получение скриншота и заголовка
        driver.get(url_user)
        title_page = driver.title
        driver.save_screenshot(name_path_file)
        driver.quit()
    except InvalidArgumentException:
        url_user = 'http://' + url_user
        try:
            #Получение скриншота и заголовка
            driver.get(url_user)
            title_page = driver.title
            driver.save_screenshot(name_path_file)
            driver.quit()
        except:
            #Время получение скриншота
            time_request = "Время обработки: %.0f сек." % (time.time() - start_time)
            return 'Не удалось открыть страницу', time_request, None, whois_text
    except WebDriverException:
        #Время получение скриншота
        time_request = "Время обработки: %.0f сек." % (time.time() - start_time)
        return 'Не удалось открыть страницу', time_request, None, whois_text
    
    #Время получение скриншота
    time_request = "Время обработки: %.0f сек." % (time.time() - start_time)

    return name_path_file, time_request, title_page, whois_text


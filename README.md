# screenshot_bot
Telegram bot sends screenshots via the requested link

### Инструкция по развёртыванию

Нужно создать файл config.py на основе config_example.py:
1. Указать токен телеграм бота.
2. Скачать драйвер для selenium: https://selenium-python.com/install-chromedriver-chrome
3. Если у вас Linux дистрибутив или Mac, вам нужно дать файлу chromedriver нужные права на выполнения. Открываем терминал и вводим команды одна за другой.
<br/>`cd /путь/до/драйвера/`
<br/>`sudo chmod +x chromedriver`
4. Путь до драйвера у Linux или Mac: '/путь/до/драйвера/chromedriver'
<br/>У Windows: 'путь\\до драйвера\\chromedriver.exe'

Нужно создать виртуальное окружение, далее пример для windows:
<br/>virtualenv — утилита для создания виртуальных окружений.
<br/>Для установки виртуального окружения:
<br/>`pip install virtualenv`
<br/>Для создания виртуального окружения:
<br/>`virtualenv <имя виртуального окружения>`
<br/>В текущем каталоге будет создана новая директория с указанным вами названием, куда будут перенесены python, pip и в дальнейшем установлены другие библиотеки.
<br/>Активация виртуального окружения:
<br/>`<имя виртуального окружения>\Scripts\activate`
<br/>Для деактивации виртуального окружения:
<br/>`deactivate`

Нужно установить все необходимые библиотеки командой: `pip install -r requirements.txt`

Запустить бот можно при помощи команды: `python bot.py`
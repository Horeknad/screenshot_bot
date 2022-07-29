# screenshot_bot
Telegram bot sends screenshots via the requested link

Инструкция по развёртыванию

Нужно создать файл config.py на основе config_example.py:
1. Указать токен телеграм бота.
2. Скачать драйвер для selenium: https://selenium-python.com/install-chromedriver-chrome
3. Если у вас Linux дистрибутив или Mac, вам нужно дать файлу chromedriver нужные права на выполнения. Открываем терминал и вводим команды одна за другой.
cd /путь/до/драйвера/
sudo chmod +x chromedriver
4. Путь до драйвера у Linux или Mac: '/путь/до/драйвера/chromedriver'
У Windows: 'путь\\до драйвера\\chromedriver.exe'

Нужно создать виртуальное окружение, далее пример для windows:
\nvirtualenv — утилита для создания виртуальных окружений.
\nДля установки виртуального окружения:
\npip install virtualenv
\nДля создания виртуального окружения:
\nvirtualenv <имя виртуального окружения>
\nВ текущем каталоге будет создана новая директория с указанным вами названием, куда будут перенесены python, pip и в дальнейшем установлены другие библиотеки.
\nАктивация виртуального окружения:
\n<имя виртуального окружения>\Scripts\activate
\nДля деактивации виртуального окружения:
\ndeactivate

Нужно установить все необходимые библиотеки командой: pip install -r requirements.txt
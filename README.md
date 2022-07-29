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
virtualenv — утилита для создания виртуальных окружений.
Для установки виртуального окружения:
pip install virtualenv
Для создания виртуального окружения:
virtualenv <имя виртуального окружения>
В текущем каталоге будет создана новая директория с указанным вами названием, куда будут перенесены python, pip и в дальнейшем установлены другие библиотеки.
Активация виртуального окружения:
<имя виртуального окружения>\Scripts\activate
Для деактивации виртуального окружения:
deactivate

Нужно установить все необходимые библиотеки командой: pip install -r requirements.txt
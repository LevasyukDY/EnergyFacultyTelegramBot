<p align="center" width="100%">
    <img width="33%" src="https://raw.githubusercontent.com/LevasyukDY/EnergyFacultyWebsite/main/src/assets/logo.png"> 
</p>

![](https://img.shields.io/github/languages/code-size/LevasyukDY/EnergyFacultyTelegramBot) 
![](https://img.shields.io/github/commit-activity/w/LevasyukDY/EnergyFacultyTelegramBot)
![](https://img.shields.io/github/last-commit/LevasyukDY/EnergyFacultyTelegramBot)

# Информационный сервис ЭФ ЗабГУ

В данном репозитории представлен исходный код телеграм бота для сайта Энергетического факультета ЗабГУ.

Исходный код frontend части сайта вы можете найти [в моём репозитории](https://github.com/LevasyukDY/EnergyFacultyWebsite).

Исходный код backend сайта вы можете найти [в репозитории](https://github.com/TseplyaevAF/energy_faculty) моего партнёра.

## Структура проекта

```
├── config.py
├── create_bot.py
├── handlers
│  ├── __init__.py
│  ├── client.py
│  └── other.py
├── keyboards
│  ├── __init__.py
│  └── client_kb.py
├── main.py
└── README.md
```

## Зависимости проекта

```
Package            Version
------------------ ---------
aiogram            2.19
aiohttp            3.8.1
aiosignal          1.2.0
async-timeout      4.0.2
attrs              21.4.0
Babel              2.9.1
certifi            2021.10.8
charset-normalizer 2.0.12
frozenlist         1.3.0
idna               3.3
multidict          6.0.2
pip                22.0.4
pytz               2022.1
requests           2.27.1
setuptools         58.1.0
soupsieve          2.3.1
urllib3            1.26.9
yarl               1.7.2
```
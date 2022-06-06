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

## To-Do

- [x] номер кабинета кафедры в контактах
- [ ] вывод картинки при уведомлении о новой записи
- [ ] расписание для заочников (дз для заочников)
- [ ] расписание экзаменов и консультаций
- [ ] голосовые команды
- [ ] схема расположения кабинетов по этажам

## Структура проекта

```
├── cenz.txt            – список нецензурных слов в обычном виде
├── cenz.json           – список нецензурных слов в зашифрованном виде
├── config.py           – файл, хранящий в себе токен бота
├── create_bot.py       – модуль, создающий экземпляр бота
├── handlers            – каталог, хранящий в себе хэндлеры бота
│  ├── __init__.py          – файл с импортом модулей client и other
│  ├── client.py            – клиентская часть для работы с ботом
│  └── other.py             – содержит хэндлер с другими менее важными командами
├── keyboards           – каталог, хранящий модуль создания кнопок
│  ├── __init__.py          – файл с импортом модуля client_kb
│  └── client_kb.py         – модуль, создающий кнопки
├── main.py             – главная точка входа
├── README.md
├── to_json.py          – скрипт, конвертирующий cenz.txt в cenz.json
└── users.txt           – список всех пользователей запустивших бота
```

## Как получить токен бота

Необходимо в телеграм найти в поиске бота всех ботов ```BotFather``` (он будет с синей галочкой) и по очереди написать ему слудующее:

```
> /start

> /newbot
```

Здесь может быть любое название вашего бота:
```
> Бот ЭФ ЗабГУ
```

Вводим ```id``` бота, по которому люди будут искать нашего бота, обязательно в конце добавить слово ```bot```:
```
> zabgu_energy_faculty_bot 
```

Далее в ответном сообщении бота мы увидим наш токен под строчкой "Use this token to access the HTTP API".

Он выглядит примерно так:
```
270485614:AAHfiqksKZ8WmR2zSjiQ7_v4TMAKdiHm9T0
```

Можно установить для бота аватар командой:
```
> /setuserpic
```

Далее выбираем id нашего бота и отправляем аватар

Также на всякий случай дадим нашему боту повышенные права доступа командой:
```
> /setprivacy
```
и параметром:
```
> Disable
```


## Зависимости проекта

Для начала работы необходимо создать виртуальное окружение в корневой папке бота командой:

```
python3 -m venv venv
```

И активировать его командой*:

```
source venv/bin/activate
```

> *Либо нажать соответствующую кнопку активации в всплывающем окне ```VS Code```.

Далее необходимо установить некоторые пакеты в виртуальное окружение, выполнив в терминале команды, указанные напротив пакетов:

```
Package            Version
------------------ ---------
aiogram            2.19         – pip install aiogram
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
requests           2.27.1       – pip install requests
setuptools         58.1.0
soupsieve          2.3.1
urllib3            1.26.9
yarl               1.7.2
```
> Остальные пакеты сами подтянутся с ```aiogram```


## Пример файла ```config.py```

```
TOKEN = '270485614:AAHfiqksKZ8WmR2zSjiQ7_v4TMAKdiHm9T0'
SERVER_URL = 'http://127.0.0.1:8000/'
WEBSITE_URL = 'http://192.168.1.6:8080/'

```

## Пример файла ```cenz.txt```

После каждого изменения в этом файле необходимо запустить скрипт ```to_json.py```

```
мат

блин

ёмаё

```
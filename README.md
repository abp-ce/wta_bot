# wta_bot
Телеграм бот.
#
### Как запустить проект:

#### Предварительные требования:
- развернутый wta_backend и Redis
- заполненныый .env, см. env.sample

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/abp-ce/wta_bot
```

```
cd wta_bot
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```
Обновить pip и установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Запустить проект:

```
python main.py
```
### Стек:
 - aiogram 3.0.0b7
 - httpx
 - redis

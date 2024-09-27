import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# API ключ кинопоиска
KINO_POISK_API_KEY = os.getenv('KINO_POISK_API_KEY')

# Путь и название базы данных
DATABASE_URL = 'sqlite+aiosqlite:///db/tg_bot_skillbox.sqlite'

# URL для запросов к API Кинопоиска
KINOPOISK_MOVIE_URL = 'https://api.kinopoisk.dev/v1.4/movie/'
KINOPOISK_PERSON_URL = 'https://api.kinopoisk.dev/v1.4/person/'

# Заголовки для запросов к API Кинопоиска
headers = {
    'accept': 'application/json',
    'X-API-KEY': KINO_POISK_API_KEY
}

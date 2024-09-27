import aiohttp

from config_data import config


async def search_actor_api(actor_name: str, limit: int) -> dict | None:
    """
    Асинхронная функция для поиска актёров по имени через API Кинопоиска.

    :param actor_name: Имя или часть имени актёра для поиска.
    :param limit: Лимит на количество результатов, которые должны быть возвращены.
    :return: Словарь с результатами поиска актёров или None в случае ошибки.
    """
    # Формируем URL для поиска с учётом лимита и запроса имени актёра
    search_url = f'{config.KINOPOISK_PERSON_URL}search?page=1&limit={limit}&query={actor_name}'

    # Заголовки для запроса, которые могут включать токены и ключи API
    request_headers = config.headers

    # Открываем асинхронную сессию для выполнения HTTP-запроса
    async with aiohttp.ClientSession() as session:
        # Выполняем GET-запрос с переданными заголовками
        async with session.get(search_url, headers=request_headers) as response:
            # Если запрос успешен (статус 200), возвращаем результат поиска в виде словаря
            if response.status == 200:
                search_results = await response.json()
                return search_results
            else:
                # В случае ошибки выводим статус и возвращаем None
                print(f'Ошибка: {response.status}')
                return None

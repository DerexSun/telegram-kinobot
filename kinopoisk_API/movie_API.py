import aiohttp

from config_data import config


async def search_movie_api(movie_name: str, limit: int) -> dict | None:
    """
    Асинхронная функция для поиска фильмов по названию через API Кинопоиска.

    :param movie_name: Название фильма или его часть для поиска.
    :param limit: Лимит на количество возвращаемых результатов.
    :return: Словарь с результатами поиска фильмов или None в случае ошибки.
    """
    # Формирование URL для поиска фильмов с учетом лимита и запроса по названию
    search_url = f'{config.KINOPOISK_MOVIE_URL}search?page=1&limit={limit}&query={movie_name}'

    # Заголовки для запроса, которые могут включать токены или ключи API
    request_headers = config.headers

    # Асинхронная сессия для выполнения HTTP-запроса
    async with aiohttp.ClientSession() as session:
        # Выполняем GET-запрос с переданными заголовками
        async with session.get(search_url, headers=request_headers) as response:
            # Если запрос успешен (статус 200), возвращаем данные в виде словаря
            if response.status == 200:
                search_results = await response.json()
                return search_results
            else:
                # В случае ошибки выводим статус и возвращаем None
                print(f'Ошибка: {response.status}')
                return None

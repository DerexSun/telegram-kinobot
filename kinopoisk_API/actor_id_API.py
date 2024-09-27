import aiohttp

from config_data import config


async def get_actor_info(actor_id: int) -> dict | None:
    """
    Асинхронная функция для получения информации об актёре с использованием API Кинопоиска.

    :param actor_id: Идентификатор актёра на Кинопоиске.
    :return: Словарь с информацией об актёре, если запрос успешен, или None в случае ошибки.
    """
    # Формируем URL для запроса к API Кинопоиска
    actor_info_url = f'{config.KINOPOISK_PERSON_URL}{actor_id}'

    # Заголовки, необходимые для аутентификации или идентификации в API
    request_headers = config.headers

    # Открываем асинхронную сессию для выполнения HTTP-запроса
    async with aiohttp.ClientSession() as session:
        # Отправляем GET-запрос с заголовками
        async with session.get(actor_info_url, headers=request_headers) as response:
            # Проверяем успешность запроса
            if response.status == 200:
                # Возвращаем данные в виде словаря
                actor_data = await response.json()
                return actor_data
            else:
                # Выводим сообщение об ошибке, если запрос не успешен
                print(f'Ошибка: {response.status}')
                return None

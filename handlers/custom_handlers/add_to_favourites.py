from aiogram import types
from aiogram.fsm.context import FSMContext

from db.db_service import add_movie_to_favourites_in_db, check_current_favorites_count


async def add_movie_to_favourites(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик для добавления фильма в избранное.

    Извлекает movie_id из callback_data, проверяет, есть ли фильм в списке
    и добавляет его в избранное пользователя, если это возможно.

    :param callback_query: Объект CallbackQuery от Aiogram.
    :param state: Объект состояния FSMContext для хранения данных.
    """
    # Извлечение movie_id из callback_data
    movie_callback_id = callback_query.data.split(':')[1]

    state_data = await state.get_data()
    movies_list = state_data.get('movies', [])

    # Находим выбранный фильм по ID
    selected_movie = next((movie for movie in movies_list if str(movie['id']) == movie_callback_id), None)

    if selected_movie:
        movie_name = selected_movie['name']
        movie_id = selected_movie['id']
        genres = selected_movie['genres']
        release_year = selected_movie['year']
        country = selected_movie['country']
        telegram_id = callback_query.from_user.id

        # Проверяем текущее количество избранных фильмов
        current_favorites_count, user_id = await check_current_favorites_count(telegram_id)

        if user_id is None:
            await callback_query.answer('Ошибка: пользователь не найден.')
            return

        if current_favorites_count >= 10:
            await callback_query.answer('Вы не можете добавить больше 10 фильмов в избранное.')
        else:
            # Добавляем фильм в избранное
            if await add_movie_to_favourites_in_db(
                    user_id=user_id,
                    movie_name=movie_name,
                    movie_id=movie_id,
                    release_year=release_year,
                    genres=genres,
                    country=country
            ):
                await callback_query.answer(f'Фильм "{movie_name}" добавлен в избранное!')
            else:
                await callback_query.answer(f'Фильм "{movie_name}" уже находится в избранном.')
    else:
        await callback_query.answer('Ошибка: не удалось найти фильм.')

    # Удаляем клавиатуру
    await callback_query.message.edit_reply_markup()

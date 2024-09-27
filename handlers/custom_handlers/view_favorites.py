from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from db.db_service import get_favourites
from keyboards.inline.create_inline_keyboard import main_menu_inline_keyboard, viewing_and_deleting_favorites


class FavoritesStates(StatesGroup):
    waiting_for_movie_number = State()


# Хендлер для показа избранных фильмов
async def favourites_callback_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает запрос на отображение избранных фильмов пользователя.

    :param callback_query: Объект CallbackQuery, содержащий информацию о запросе.
    :param state: Контекст состояния для хранения данных о пользователе.
    """
    await state.clear()  # Очищаем предыдущее состояние
    telegram_id = callback_query.from_user.id

    # Получаем избранные фильмы через DataBaseManager
    favourites = await get_favourites(telegram_id)

    if not favourites:
        await callback_query.answer('Ваше избранное пусто!', reply_markup=main_menu_inline_keyboard())
        return

    await callback_query.answer('Ваше избранное')
    message_text = 'Ваши избранные фильмы:\n'
    movie_id = None
    for movie_id, movie in enumerate(favourites, 1):
        message_text += (f'{movie_id}. <code>{movie.movie_name}</code> - ({movie.release_year}), '
                         f'Жанр: <i>{movie.genres}</i>, Страна: {movie.country}\n')

    await callback_query.message.answer(message_text, reply_markup=viewing_and_deleting_favorites(movie_id))
    await state.update_data(favourites=favourites)

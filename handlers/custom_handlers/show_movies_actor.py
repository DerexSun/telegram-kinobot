from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.create_inline_keyboard import main_menu_inline_keyboard


async def handle_show_movies_actor(callback_query: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает запрос на отображение фильмов актера.

    :param callback_query: Объект CallbackQuery, содержащий информацию о запросе.
    :param state: Контекст состояния Finite State Machine для доступа к данным.
    """
    await callback_query.answer()
    data = await state.get_data()
    actor_info = data.get('actor_info')

    if actor_info and 'movies' in actor_info:
        movies_list = '\n'.join(
            f'<code>{movie['name']}</code> (⭐{movie.get('rating', 'Нет данных')})'
            for movie in actor_info['movies'] if movie.get('name')
        )
        # Считаем количество символов и разделяем на несколько сообщений
        _max_length = 4096  # Максимальная длина сообщения в телеграмм
        if len(movies_list) > _max_length:
            parts = []
            current_part = ''

            for movie in movies_list.split('\n'):
                if len(current_part) + len(movie) + 1 <= _max_length:
                    current_part += (movie + '\n')
                else:
                    parts.append(current_part)
                    current_part = movie + '\n'

            if current_part:
                parts.append(current_part)

            await callback_query.message.answer(f'Найденные фильмы для: {actor_info['name']}:',
                                                parse_mode='HTML')
            for part in parts:
                await callback_query.message.answer(part.strip(), parse_mode='HTML',
                                                    reply_markup=main_menu_inline_keyboard())
        else:
            await callback_query.message.answer(f'Найденные фильмы для: {actor_info['name']}:\n{movies_list}',
                                                parse_mode='HTML', reply_markup=main_menu_inline_keyboard())
    else:
        await callback_query.message.answer('Не удалось найти фильмы для актёра.',
                                            reply_markup=main_menu_inline_keyboard())

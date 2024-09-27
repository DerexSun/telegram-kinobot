import asyncio
import re
from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from keyboards.inline.create_inline_keyboard import (
    main_menu_inline_keyboard,
    move_favourites_keyboard,
    create_limit_search_keyboard
)
from kinopoisk_API.movie_API import search_movie_api


class MovieSearchStates(StatesGroup):
    """
    Состояния для поиска фильма.
    """
    waiting_for_movie_name = State()
    waiting_for_movie_limit = State()


async def handle_movie_search(callback_query: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает команду поиска фильма.

    :param callback_query: Объект CallbackQuery от пользователя, инициировавшего команду.
    :param state: Контекст состояния Finite State Machine для сохранения данных.
    """
    await state.clear()
    await callback_query.answer()
    await callback_query.message.answer('Введите название фильма для поиска:')
    await state.set_state(MovieSearchStates.waiting_for_movie_name)


async def process_movie_name(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает введенное название фильма и запрашивает лимит на количество фильмов для поиска.

    :param message: Сообщение от пользователя с названием фильма.
    :param state: Контекст состояния Finite State Machine для сохранения данных.
    """
    movie_name = message.text
    # Удаляет из строки `movie_name` все символы, кроме букв (латинских и кириллических), цифр, дефиса и пробелов.
    # Это используется для очистки названия фильма от нежелательных символов (например, пунктуации или спецсимволов).
    clean_movie_name = re.sub(r'[^A-Za-zА-Яа-я0-9\- ]+', '', movie_name)

    # Сохраняем название фильма в состояние
    await state.update_data(movie_name=clean_movie_name)

    # Спрашиваем пользователя, сколько фильмов искать
    limit_message = await message.answer('Сколько фильмов искать?', reply_markup=create_limit_search_keyboard())
    # Сохраняем сообщение в состояние для последующего удаления
    await state.update_data(limit_message_id=limit_message.message_id)
    await state.set_state(MovieSearchStates.waiting_for_movie_limit)


async def process_movie_limit(callback_query: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает выбранный лимит для поиска фильмов и выполняет поиск.

    :param callback_query: Объект CallbackQuery от пользователя с выбранным лимитом.
    :param state: Контекст состояния Finite State Machine для сохранения данных.
    """
    await callback_query.answer()

    # Извлекаем количество фильмов из callback_data
    limit = int(callback_query.data.split('_')[1])

    # Получаем сохраненное название фильма из состояния
    data = await state.get_data()
    movie_name = data.get('movie_name')

    # Удаляем сообщение с вопросом о лимите, если оно было отправлено
    limit_message_id = data.get('limit_message_id')
    if limit_message_id:
        await callback_query.message.bot.delete_message(chat_id=callback_query.message.chat.id,
                                                        message_id=limit_message_id)

    # Отправляем сообщение о начале поиска
    searching_message = await callback_query.message.answer('Начинаю поиск, подождите!')

    # Выполняем запрос к API с учетом выбранного лимита
    movie_data = await search_movie_api(movie_name, limit=limit)  # Передаем лимит в API

    await searching_message.delete()

    if movie_data and movie_data['docs']:
        # Инициализируем список для сохранения данных о фильмах
        movies = []

        for movie_info in movie_data['docs']:
            poster_url = movie_info['poster']['url'] if movie_info['poster'] else None
            description = movie_info['description']
            genres = ', '.join(genre['name'] for genre in movie_info['genres'])
            country = ', '.join(country['name'] for country in movie_info['countries'])

            # Добавляем информацию о фильме в список
            movies.append({'name': movie_info['name'], 'year': movie_info['year'], 'genres': genres,
                           'country': country, 'id': movie_info['id']})

            caption = (
                f'🎬 <i><b>Название:</b></i> {movie_info['name']}\n'
                f'📅 <i><b>Год:</b></i> {movie_info['year']}\n'
                f'📝 <i><b>Описание:</b></i> {description}\n'
                f'🎭 <i><b>Жанры:</b></i> {genres}\n'
                f'🌍 <i><b>Страна:</b></i> {country}\n'
                f'<i><b>Рейтинг:</b></i>\n'
                f'⭐<i><b>Кп:</b></i> {movie_info['rating']['kp']} '
                f'⭐<i><b>imdb:</b></i> {movie_info['rating']['imdb']} '
                f'⭐<i><b>FC:</b></i> {movie_info['rating']['filmCritics']} '
                f'⭐<i><b>RFC:</b></i> {movie_info['rating']['russianFilmCritics']}'
            )

            # Проверяем длину caption и обрезаем description при необходимости
            _max_caption_length = 1024
            if len(caption) > _max_caption_length:
                excess_length = len(caption) - _max_caption_length
                description = description[:-excess_length].rstrip() + '...'  # Обрезаем и добавляем многоточие
                caption = caption.replace(movie_info['description'], description)

            # Отправляем постер и описание
            if poster_url:
                await callback_query.message.answer_photo(photo=poster_url, caption=caption, parse_mode='HTML',
                                                          reply_markup=move_favourites_keyboard(movie_info))
            else:
                await callback_query.message.answer(caption, parse_mode='HTML',
                                                    reply_markup=move_favourites_keyboard(movie_info))

            await asyncio.sleep(1)  # Задержка в 1 секунду

        # Сохраняем список фильмов в FSMContext
        await state.update_data(movies=movies)

        # Отправляем сообщение с основным меню
        await callback_query.message.answer('Все фильмы отправлены. Выберите действие:',
                                            reply_markup=main_menu_inline_keyboard())

    else:
        await callback_query.message.answer(f'Не удалось найти информацию о фильме\n"<i><b>{movie_name}</b></i>".',
                                            reply_markup=main_menu_inline_keyboard())
        await state.clear()

import asyncio
import re

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from keyboards.inline.create_inline_keyboard import (
    main_menu_inline_keyboard,
    create_limit_search_keyboard,
    actor_details_keyboard
)
from kinopoisk_API.actor_name_API import search_actor_api


class ActorSearchStatesName(StatesGroup):
    """
    Класс для управления состоянием поиска актера.
    Содержит состояния для ожидания ввода имени актера и лимита фильмов.
    """
    waiting_for_actor_name = State()  # Ожидание имени актера
    waiting_for_actor_limit = State()  # Ожидание лимита фильмов


async def handle_actor_search_name(callback_query: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик для начала поиска актера.
    Очищает состояние и запрашивает имя актера у пользователя.

    :param callback_query: Объект CallbackQuery от Aiogram.
    :param state: Объект состояния FSMContext.
    """
    await state.clear()  # Очищаем предыдущее состояние
    await callback_query.answer()  # Подтверждаем получение колбэка
    await callback_query.message.answer('Введите имя для поиска:')  # Запрашиваем имя актера
    await state.set_state(ActorSearchStatesName.waiting_for_actor_name)  # Устанавливаем новое состояние


async def process_actor_name(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения имени актера от пользователя.
    Очищает имя от нежелательных символов и запрашивает лимит фильмов.

    :param message: Объект Message от Aiogram.
    :param state: Объект состояния FSMContext.
    """
    actor_name = message.text  # Сохраняем текст сообщения
    # Удаляет из строки `actor_name` все символы, кроме букв (латинских и кириллических), цифр, дефиса и пробелов.
    # Это используется для очистки имени от нежелательных символов (например, пунктуации или спецсимволов).
    cleaned_actor_name = re.sub(r'[^A-Za-zА-Яа-я0-9\- ]+', '',
                                actor_name)  # Очищаем имя от нежелательных символов

    # Сохраняем имя актера в состояние
    await state.update_data(actor_name=cleaned_actor_name)

    # Спрашиваем пользователя, сколько фильмов искать
    limit_message = await message.answer('Сколько вариантов искать?', reply_markup=create_limit_search_keyboard())
    # Сохраняем сообщение в состояние для последующего удаления
    await state.update_data(limit_message_id=limit_message.message_id)
    await state.set_state(ActorSearchStatesName.waiting_for_actor_limit)  # Устанавливаем новое состояние


async def process_actor_search(callback_query: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик для выполнения поиска актера по имени.
    Извлекает количество фильмов, запрашивает данные у API и отправляет результаты пользователю.

    :param callback_query: Объект CallbackQuery от Aiogram.
    :param state: Объект состояния FSMContext.
    """
    await callback_query.answer()  # Подтверждаем получение колбэка

    # Извлекаем количество фильмов из callback_data
    limit = int(callback_query.data.split('_')[1])

    # Получаем сохраненное имя актера из состояния
    data = await state.get_data()
    actor_name = data.get('actor_name')

    # Удаляем сообщение с вопросом о лимите, если оно было отправлено
    limit_message_id = data.get('limit_message_id')
    if limit_message_id:
        await callback_query.message.bot.delete_message(chat_id=callback_query.message.chat.id,
                                                        message_id=limit_message_id)

    # Отправляем сообщение о начале поиска
    searching_message = await callback_query.message.answer('Начинаю поиск, подождите!')

    # Выполняем запрос к API с учетом выбранного лимита
    actor_data = await search_actor_api(actor_name, limit=limit)

    # Удаляем сообщение о начале поиска
    await searching_message.delete()

    # Получаем текущий список сообщений из состояния
    sent_messages = data.get('sent_messages', [])

    # Обрабатываем ответ от API
    if actor_data and 'docs' in actor_data and actor_data['docs']:

        for actor_info in actor_data['docs']:
            _actor_id = actor_info.get('id')  # ID актера
            poster_url = actor_info.get('photo')  # URL постера
            actor_birthday = actor_info.get('birthday')  # Дата рождения актера
            formatted_birthday = actor_birthday.split('T')[
                0] if actor_birthday else 'Не указано'  # Форматируем дату рождения

            # Определяем возраст и его правильное склонение
            age = actor_info.get('age', None)
            if age is not None:
                if age % 10 == 1 and age % 100 != 11:
                    age_suffix = 'год'
                elif age % 10 in [2, 3, 4] and not (age % 100 in [12, 13, 14]):
                    age_suffix = 'года'
                else:
                    age_suffix = 'лет'
            else:
                age_suffix = 'Не указано'

            # Формируем текстовое сообщение об актере
            actor_caption = (
                f'<i><b>Имя:</b></i> {actor_info.get('name', 'Не указано')}\n'
                f'<i><b>Английское имя:</b></i> {actor_info.get('enName', 'Не указано')}\n'
                f'<i><b>Пол:</b></i> {actor_info.get('sex', 'Не указано')}\n'
                f'<i><b>Рост:</b></i> {actor_info.get('growth', 'Не указано')} см\n'
                f'<i><b>Дата рождения:</b></i> {formatted_birthday}\n'
                f'<i><b>Возраст:</b></i> {age} {age_suffix}\n'
            )

            # Отправляем постер и описание
            if poster_url:
                message_sent = await callback_query.message.answer_photo(photo=poster_url, caption=actor_caption,
                                                                         parse_mode='HTML',
                                                                         reply_markup=actor_details_keyboard(
                                                                             actor_info))
            else:
                message_sent = await callback_query.message.answer(actor_caption, parse_mode='HTML',
                                                                   reply_markup=actor_details_keyboard(
                                                                       actor_info))

            # Сохраняем отправленное сообщение в список
            sent_messages.append(message_sent)

            await asyncio.sleep(1)  # Задержка в 1 секунду

        # Отправляем сообщение с основным меню
        await callback_query.message.answer('Все актеры отправлены. Выберите действие:',
                                            reply_markup=main_menu_inline_keyboard())

    else:
        await callback_query.message.answer(f'Не удалось найти информацию о человеке\n"<i><b>{actor_name}</b></i>".',
                                            reply_markup=main_menu_inline_keyboard())
        await state.clear()  # Очищаем состояние

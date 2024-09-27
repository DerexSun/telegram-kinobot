from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.create_inline_keyboard import show_movies_actor_keyboard
from kinopoisk_API.actor_id_API import get_actor_info


async def get_actor_details(callback_query: CallbackQuery, state: FSMContext):
    """
    Обработчик для получения информации об актере по его ID.
    Извлекает actor_id из callback_data, получает информацию об актере
    и передает ее для дальнейшей обработки.

    :param callback_query: Объект CallbackQuery от Aiogram.
    :param state: Объект состояния FSMContext для хранения данных.
    """
    # Извлечение actor_id из callback_data
    actor_callback_id = callback_query.data.split(':')[1]
    actor_info = await get_actor_info(int(actor_callback_id))

    if actor_info:
        await process_actor_info(actor_info, callback_query, state)

    await callback_query.message.edit_reply_markup()  # Удаляем клавиатуру
    await callback_query.message.delete()  # Удаляем сообщение


async def process_actor_info(actor_info, callback_query: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает информацию об актере и формирует сообщение с ее отображением.

    :param actor_info: Словарь с информацией об актере.
    :param callback_query: Объект CallbackQuery от Aiogram.
    :param state: Объект состояния FSMContext для хранения данных.
    """
    # Получение и форматирование данных актера
    actor_birthday = actor_info.get('birthday')
    formatted_birthday = actor_birthday.split('T')[0] if actor_birthday else 'Не указано'
    birth_places = ', '.join([place['value'] for place in actor_info.get('birthPlace', [])]) or 'Не указано'

    # Получение даты смерти
    actor_death = actor_info.get('death')
    formatted_death = actor_death.split('T')[0] if actor_death else 'Не указано'

    # Обработка данных о супруге
    spouses = actor_info.get('spouses', [])
    spouses_info = []
    for spouse in spouses:
        relation = spouse.get('relation', 'Не указано')
        divorce_status = 'в разводе' if spouse.get('divorced', False) else 'в браке'
        children_count = spouse.get('children', 'нет')
        spouses_info.append(f'{relation} ({divorce_status}, дети: {children_count})')

    spouses_caption = ', '.join(spouses_info) if spouses_info else 'Нет данных'

    # Получение интересных фактов об актере
    facts = [fact['value'] for fact in actor_info.get('facts', [])]
    facts_caption = '\n'.join(
        [f'📝 <i><b>Факт {i + 1}:</b></i> {fact}' for i, fact in enumerate(facts)]) if facts else 'Нет интересных фактов'

    # Обработка возраста
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

    # Обработка количества наград
    awards_count = actor_info.get('countAwards')
    awards_count_caption = awards_count if awards_count is not None else 'Нет данных'

    # Формируем описание актера
    actor_caption = (
        f'🎭 <i><b>Имя:</b></i> {actor_info.get('name', 'Не указано')}\n'
        f'🌍 <i><b>Английское имя:</b></i> {actor_info.get('enName', 'Не указано')}\n'
        f'⚤ <i><b>Пол:</b></i> {'♂️ Мужчина' if actor_info.get('sex') == 'Мужской' else '♀️ Женщина' if actor_info.get('sex') == 'Женский' else 'Не указано'}\n'
        f'📏 <i><b>Рост:</b></i> {actor_info.get('growth', 'Не указано')} см\n'
        f'🎂 <i><b>Дата рождения:</b></i> {formatted_birthday}\n'
        f'🪦 <i><b>Дата смерти:</b></i> {formatted_death}\n'
        f'🎉 <i><b>Возраст:</b></i> {age} {age_suffix}\n'
        f'🗺️ <i><b>Место рождения:</b></i> {birth_places}\n'
        f'🏆 <i><b>Количество наград:</b></i> {awards_count_caption}\n'
        f'💍 <i><b>Супруги:</b></i> {spouses_caption}\n'
        f'{facts_caption}\n'
    )

    # Отправляем сообщение с постером актера
    poster_url = actor_info.get('photo', None)
    if poster_url:
        await callback_query.message.answer_photo(photo=poster_url)
        await callback_query.message.answer(actor_caption, parse_mode='HTML', reply_markup=show_movies_actor_keyboard())
    else:
        await callback_query.message.answer(actor_caption, parse_mode='HTML', reply_markup=show_movies_actor_keyboard())

    # Сохраняем информацию об актёре в состоянии, чтобы потом использовать её для показа фильмов
    await state.update_data(actor_info=actor_info)

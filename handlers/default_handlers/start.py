from aiogram import types

from db.db_service import add_or_update_user
from keyboards.inline.create_inline_keyboard import main_menu_inline_keyboard


async def start_command(message: types.Message) -> None:
    """
    Обрабатывает команду старт и отправляет приветственное сообщение пользователю.

    :param message: Объект Message, содержащий информацию о сообщении и пользователе.
    """
    user = message.from_user
    first_name = user.first_name or None
    last_name = user.last_name or None
    username = user.username or None

    # Отправка приветствия с HTML-разметкой
    if first_name or last_name:
        greeting = f'Привет! <b>{first_name or ""}</b> <b>{last_name or ""}</b>'
    else:
        greeting = 'Привет! Добрый человек!'

    # Отправка сообщения
    await message.answer(
        f'{greeting}\n'
        f'🎬 <b>КиноБот</b> — твой персональный гид по миру кино!\n\n'
        f'🔍 <b>Возможности:</b>\n\n'
        f'• Поиск фильмов прямо с Кинопоиска 🎞️\n'
        f'• Добавление любимых фильмов в избранное ⭐\n'
        f'• Поиск актеров и режиссеров по имени 👤\n'
        f'• Просмотр детальной информации об актерах: дата рождения, биография, фильмография 📚\n'
        f'• Фильмы, в которых участвовал выбранный актер 🎥\n\n'
        f'Найдите новые фильмы, узнайте больше о любимых актерах и создавайте свое персональное киноизбранное — все в одном месте!',
        parse_mode='HTML',
        reply_markup=main_menu_inline_keyboard()
    )

    await add_or_update_user(user.id, username, first_name, last_name)

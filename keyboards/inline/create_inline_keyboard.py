from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Создаем класс CallbackData для удаления фильма
class DeleteMovieCallback(CallbackData, prefix='delete_movie'):
    movie_id: int


def main_menu_inline_keyboard() -> types.InlineKeyboardMarkup:
    """
    Создает клавиатуру главного меню с основными функциями.

    :return: InlineKeyboardMarkup для главного меню.
    """
    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text='🔍 Поиск фильма', callback_data='move_search'),
            types.InlineKeyboardButton(text='👤 Поиск актёра', callback_data='name_search'),
        ],
        [
            types.InlineKeyboardButton(text='⭐ Избранное', callback_data='favourites'),
            types.InlineKeyboardButton(text='❓ Помощь', callback_data='help_command'),
        ],
    ])
    return inline_keyboard


def back_to_main_menu_keyboard() -> types.InlineKeyboardButton:
    """
    Создает кнопку для возврата в главное меню.

    :return: InlineKeyboardButton для возврата в главное меню.
    """
    return types.InlineKeyboardButton(text='🏠 Главное меню', callback_data='main_menu')


def create_limit_search_keyboard() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для выбора количества фильмов для поиска.

    :return: InlineKeyboardMarkup с кнопками для выбора лимита.
    """
    limits = [1, 3, 5, 10, 15, 20]  # Список вариантов количества для поиска
    builder = InlineKeyboardBuilder()  # Создаем билдер для клавиатуры

    # Добавляем кнопки с соответствующими значениями
    for limit in limits:
        builder.row(
            InlineKeyboardButton(
                text=f'{limit}',
                callback_data=f'limit_{limit}'  # Callback data для обработки
            )
        )

    # Настраиваем, чтобы в каждой строке было не более 3 кнопок
    builder.adjust(3)
    return builder.as_markup()  # Возвращаем объект InlineKeyboardMarkup


def move_favourites_keyboard(movie_info: dict) -> types.InlineKeyboardMarkup:
    """
    Создает клавиатуру с возможностью добавить фильм в избранное.

    :param movie_info: Информация о фильме в виде словаря.
    :return: InlineKeyboardMarkup для добавления фильма в избранное.
    """
    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text='⭐ Добавить в избранное',
                                       callback_data=f'add_to_favourites:{str(movie_info['id'])}')
        ],
        # [back_to_main_menu_keyboard()],
    ])
    return inline_keyboard


def actor_details_keyboard(actor_info: dict) -> types.InlineKeyboardMarkup:
    """
    Создает клавиатуру для отображения деталей актера.

    :param actor_info: Информация об актере в виде словаря.
    :return: InlineKeyboardMarkup для получения детальной информации об актере.
    """
    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text='📜 Детальная информация',
                                       callback_data=f'actor_details:{str(actor_info['id'])}')
        ],
    ])
    return inline_keyboard


def viewing_and_deleting_favorites(idx: int) -> types.InlineKeyboardMarkup:
    """
    Создает клавиатуру для просмотра и удаления избранных фильмов.

    :param idx: Индекс фильма в списке избранных.
    :return: InlineKeyboardMarkup для удаления фильма из избранного.
    """
    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text='❌ Удалить из избранного',
                                       callback_data=DeleteMovieCallback(movie_id=str(idx)).pack())
        ],
        [back_to_main_menu_keyboard()],
    ])
    return inline_keyboard


def show_movies_actor_keyboard() -> types.InlineKeyboardMarkup:
    """
    Создает клавиатуру для показа фильмов актера.

    :return: InlineKeyboardMarkup для отображения фильмов актера.
    """
    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text='🎥 Показать фильмы', callback_data='show_movies')
        ],
        [back_to_main_menu_keyboard()],
    ])
    return inline_keyboard


def clear_all_favorites_keyboard() -> types.InlineKeyboardMarkup:
    """
    Создает клавиатуру для очистки всех избранных фильмов.

    :return: InlineKeyboardMarkup для удаления всех избранных фильмов.
    """
    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text='🗑️ Очистить избранное', callback_data='clear_favorites'),
            types.InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel_deletion'),
        ]
    ])
    return inline_keyboard

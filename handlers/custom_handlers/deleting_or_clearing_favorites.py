from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from db.db_service import delete_movies, clear_all_favourites
from handlers.custom_handlers.view_favorites import FavoritesStates
from keyboards.inline.create_inline_keyboard import main_menu_inline_keyboard, clear_all_favorites_keyboard


async def delete_movie_callback_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    """
    Хендлер для удаления фильма из избранного.

    Отправляет пользователю сообщение с просьбой ввести номер(а) фильма(ов),
    который(е) он хочет удалить из избранного.

    :param callback_query: Объект CallbackQuery от Aiogram, содержащий данные о событии.
    :param state: Контекст состояния для хранения временных данных.
    """
    await callback_query.answer()

    await callback_query.message.answer(
        'Введите номер фильма или несколько номеров через запятую, '
        'которые вы хотите удалить из избранного:',
        reply_markup=clear_all_favorites_keyboard()
    )
    await state.set_state(FavoritesStates.waiting_for_movie_number)


async def clear_favorites_callback_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик для очистки всех избранных фильмов.

    Удаляет все фильмы из избранного и уведомляет пользователя.

    :param callback_query: Объект CallbackQuery от Aiogram, содержащий данные о событии.
    :param state: Контекст состояния для хранения временных данных.
    """
    await callback_query.answer()

    # Получаем идентификатор пользователя
    telegram_id = callback_query.from_user.id
    await clear_all_favourites(telegram_id)

    await callback_query.message.edit_text(
        'Ваши избранные фильмы успешно очищены.',
        reply_markup=main_menu_inline_keyboard()
    )
    await state.clear()


async def cancel_deletion_callback_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик для отмены удаления фильмов из избранного.

    Уведомляет пользователя об отмене удаления и возвращает к главному меню.

    :param callback_query: Объект CallbackQuery от Aiogram, содержащий данные о событии.
    :param state: Контекст состояния для хранения временных данных.
    """
    await callback_query.answer()
    await callback_query.message.edit_text('Удаление отменено.', reply_markup=main_menu_inline_keyboard())
    await state.clear()


async def delete_movie_by_number(message: Message, state: FSMContext) -> None:
    """
    Обработчик для удаления фильмов по номерам.

    Принимает номера фильмов от пользователя и удаляет указанные фильмы из избранного.

    :param message: Объект Message от Aiogram, содержащий текст сообщения пользователя.
    :param state: Контекст состояния для хранения временных данных.
    """
    movie_numbers_str = message.text

    try:
        # Преобразуем введенные номера фильмов в список целых чисел
        movie_numbers = [int(num.strip()) for num in movie_numbers_str.split(',')]
    except ValueError:
        await message.answer(
            'Пожалуйста, введите корректные номера через запятую.',
            reply_markup=clear_all_favorites_keyboard()
        )
        return

    data = await state.get_data()
    favourites = data.get('favourites', [])

    # Проверяем на наличие некорректных номеров фильмов
    invalid_numbers = [num for num in movie_numbers if num < 1 or num > len(favourites)]
    if invalid_numbers:
        await message.answer(
            f'Фильмы с номерами {", ".join(map(str, invalid_numbers))} не найдены.',
            reply_markup=main_menu_inline_keyboard()
        )
        return

    # Удаляем фильмы из избранного
    deleted_movies = await delete_movies(favourites, movie_numbers)

    deleted_movies_list = ', '.join(deleted_movies)
    await message.answer(
        f'Фильмы "{deleted_movies_list}" успешно удалены из избранного.',
        reply_markup=main_menu_inline_keyboard()
    )
    await state.clear()

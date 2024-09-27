from aiogram.types import CallbackQuery

from keyboards.inline.create_inline_keyboard import main_menu_inline_keyboard


async def back_to_main_menu(callback_query: CallbackQuery) -> None:
    """
    Обработчик для возврата к главному меню.

    Обновляет клавиатуру сообщения, возвращая основную клавиатуру,
    чтобы пользователь мог выбрать другое действие.

    :param callback_query: Объект CallbackQuery от Aiogram, содержащий данные о событии.
    """
    # Возвращаем основную клавиатуру
    await callback_query.message.edit_reply_markup(reply_markup=main_menu_inline_keyboard())

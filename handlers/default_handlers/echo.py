from aiogram import types


async def echo_handler(message: types.Message) -> None:
    """
    Обработчик отправляет текстовое сообщение в ответ на любое текстовое сообщение.

    :param message: Объект Message от Aiogram, содержащий текстовое сообщение от пользователя.
    """
    try:
        await message.answer('Просто текстовое сообщение для команды /help')
        # Удаляем сообщение пользователя (раскомментируйте, если нужно)
        # await message.delete()
    except TypeError:
        # Обработка ошибок при попытке удалить сообщение пользователя
        # await message.delete()  # Удаляем сообщение пользователя (раскомментируйте, если нужно)
        await message.answer('Хорошая попытка! /help')

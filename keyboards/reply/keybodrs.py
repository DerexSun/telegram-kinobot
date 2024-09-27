from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Создание клавиатуры
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='ПОИСК ФИЛЬМА'), KeyboardButton(text='ПОИСК АКТЕРА')],
        [KeyboardButton(text='ПОМОЩЬ')]
    ],
    resize_keyboard=True
)

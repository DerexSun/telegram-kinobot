import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from config_data import config
from db import init_db
from handlers import handlers
from handlers.default_handlers import help, start

TOKEN = config.TELEGRAM_BOT_TOKEN

# Создаем хранилище для состояний
storage = MemoryStorage()

# Инициализация диспетчера с хранилищем
dp = Dispatcher(storage=storage)


# Асинхронный вызов инициализации базы данных
async def setup_db():
    await init_db()


# Обработка команды /start
@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await start.start_command(message)


# Обработка команды /help
@dp.message(Command('help'))
async def cmd_help(message: Message) -> None:
    await help.help_command(message)


async def main() -> None:
    # Вызов функции инициализации базы данных
    await setup_db()

    # Инициализируем бота
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Регистрируем обработчики
    registry = handlers.HandlerRegistry(dp)
    registry.register_all_handlers(dp)

    # Стартуем бот
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    try:
        print('Программа запущена.\n')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\nПрограмма была прервана.')

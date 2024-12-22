import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import router
from models import async_main

async def main():
    await async_main()  # Создаем таблицы в базе данных
    load_dotenv()  # Загружаем переменные окружения
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher(storage=MemoryStorage())  # Используем память для хранения состояний

    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')

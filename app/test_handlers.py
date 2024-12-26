import pytest
from aiogram.types import Message
from handlers import cmd_start, cmd_books
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_cmd_start():
    """Тест для команды /start."""
    message = AsyncMock()
    await cmd_start(message)
    # Проверяем, что бот отправил правильный ответ
    message.answer.assert_called_once_with(
        "Привет! Я бот для обслуживания библиотеки.\n"
        "Вот что я могу:\n"
        "/count_books - Посчитать количество экземпляров книги в филиале.\n"
        "/count_faculties - Посчитать факультеты, на которых используется книга в филиале.\n"
        "/add_book - Добавить новую книгу в библиотеку.\n"
        "/add_branch - Добавить новый филиал в библиотеку.\n"
        "/edit_book - Изменить информацию о книге.\n"
        "/edit_branch - Изменить информацию о филиале.\n"
        "/books - Вывести список книг\n"
    )

@pytest.mark.asyncio
async def test_cmd_books():
    """Тест для команды /books."""
    message = AsyncMock()
    async def mock_session_execute(*args, **kwargs):
        class MockResult:
            def scalars(self):
                class MockScalar:
                    def all(self):
                        return []
                return MockScalar()
        return MockResult()
    # Мокаем сессию базы данных
    from models import async_session
    async_session.execute = mock_session_execute
    await cmd_books(message)
    message.answer.assert_called_once_with("📚 Нет доступных книг в библиотеке.")

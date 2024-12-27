FROM python:3.9-slim

# Устанавливаем переменные окружения для Python
ENV PYTHONUNBUFFERED=1
ENV SQLALCHEMY_URL=postgresql+asyncpg://postgres:admin@database:5432/library

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запуск тестов с использованием pytest
RUN pytest --maxfail=1 --disable-warnings -q

# Команда для запуска приложения
CMD ["python", "main.py"]

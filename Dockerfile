# Используем официал ьный образ Python
FROM python:3.9-slim

# Устанавливаем переменную окружения для Python
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости из requirements.txt (убедитесь, что requirements.txt существует)
RUN pip install --no-cache-dir -r requirements.txt

# Убедитесь, что необходимые переменные окружения переданы

ENV TOKEN=7960682573:AAG0RIa7XhWIkooi9TPzrYwAwT-M8WjUVDQ
ENV SQLALCHEMY_URL=postgresql+asyncpg://postgres:admin@localhost/library

# Команда для запуска приложения
CMD ["python", "main.py"]


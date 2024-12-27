# Используем официальный образ Python
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект в контейнер
COPY . .

# Добавляем команду для ожидания готовности базы данных
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Отдельный этап для запуска тестов
RUN pytest --disable-warnings --maxfail=1 --cov=app --cov-report=xml || exit 1

CMD ["/wait-for-it.sh", "database:5432", "--", "python", "main.py"]

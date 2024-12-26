#Используем официал ьный образ Python  
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

# Команда для запуска приложения
CMD ["python", "main.py"]


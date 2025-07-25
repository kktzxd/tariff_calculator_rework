# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только requirements.txt сначала для кэширования
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

EXPOSE 8008
# Команда запуска для Django
CMD ["python3", "tariff_calculator/manage.py", "runserver", "0.0.0.0:8008"]
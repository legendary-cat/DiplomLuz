FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем не-root пользователя для безопасности
RUN useradd -m -u 1000 user
USER user

# Открываем порт
EXPOSE 8000

# Команда для запуска FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
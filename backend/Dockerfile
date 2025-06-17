# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 1) Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copy the rest of your Django code
COPY . .

# 3) Expose & run
EXPOSE 8000

# Run migrations then start the dev server
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]

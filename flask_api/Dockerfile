FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expunem portul corect (3101)
EXPOSE 3101

CMD ["python3", "app.py"]

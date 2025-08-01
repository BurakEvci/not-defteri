FROM python:3.9-slim

RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["./wait-for-it.sh", "db:5432", "--", "python", "app.py"]

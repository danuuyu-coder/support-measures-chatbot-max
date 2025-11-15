FROM python:3.11-alpine

WORKDIR /bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --progress-bar off

COPY . .

CMD ["python", "-m", "src.main"]
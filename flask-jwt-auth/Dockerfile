FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip cache purge && pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=src/app.py
ENV FLASK_ENV=development
ENV PYTHONPATH=/app

CMD ["python", "src/app.py"]
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_sm

COPY . .


ENV NAME World

CMD ["gunicorn", "-b", ":8080", "app:app"]
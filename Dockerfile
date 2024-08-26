FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt ./
RUN python -m venv .venv && source .venv/bin/activate
RUN pip install -r requirements.txt

COPY db/ ./db
COPY services/ ./services

EXPOSE 5000

CMD ["python", "./services/products-auth.py"]
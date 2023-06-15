FROM python:3.11-slim

WORKDIR /usr/src/irss-backend

COPY ./requirements.lock .

RUN sed '/-e/d' requirements.lock > requirements.lock

RUN pip install --no-cache-dir --upgrade -r requirements.lock

COPY ./app /usr/src/irss-backend/app

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80","--reload"]
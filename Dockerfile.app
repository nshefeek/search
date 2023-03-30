FROM python:3.11-slim

WORKDIR .

COPY ./requirements.txt /app/requirements.txt

RUN apt update && apt -y install gcc python3-dev musl-dev libffi-dev postgresql-server-dev-all

RUN pip install --upgrade pip
RUN pip install -U pip && \
    pip install -U -r /app/requirements.txt

COPY  ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
FROM python:3.8.3
MAINTAINER Blaine Smith

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

RUN apt-get update && apt-get install -y netcat

ENV APP=/app
WORKDIR /app

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

COPY ./app /app

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "backend.wsgi"]
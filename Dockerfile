# syntax=docker/dockerfile:1
FROM python:3.11.2-bullseye
WORKDIR /makeup_app/
COPY requirements.txt /makeup_app/
RUN pip install -r requirements.txt
COPY . /makeup_app
WORKDIR /makeup_app/permanent_makeup
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate
CMD ["gunicorn", "-b", "0.0.0.0:8000", "permanent_makeup.wsgi"]
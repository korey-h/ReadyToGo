FROM python:3.8.5
RUN  apt update
RUN  apt install nano
RUN mkdir /code
WORKDIR /code
COPY ./requirements.txt .
COPY ./ReadyToGo .
RUN pip3 install -r requirements.txt --no-cache-dir
RUN python manage.py collectstatic
CMD gunicorn StartLine.wsgi:application --bind 0.0.0.0:8001
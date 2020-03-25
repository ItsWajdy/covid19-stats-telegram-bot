From python:3.7

RUN pip install python-telegram-bot
RUN pip install pandas
RUN pip install bs4
RUN pip install requests

RUN mkdir /app
ADD . /app
WORKDIR /app

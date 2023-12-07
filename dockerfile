FROM python:3.10-alpine
WORKDIR /code
COPY requirements.txt /code
RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apk upgrade
RUN apk add mariadb
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ./code /code
CMD python app.py
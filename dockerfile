FROM python:3.10-alpine
WORKDIR /code
COPY requirements.txt /code
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ./code /code
CMD python app.py
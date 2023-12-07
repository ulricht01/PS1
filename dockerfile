# Use Python Alpine as the base image
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /code

# Install system dependencies
RUN apk update && \
    apk add --no-cache mariadb-connector-c-dev build-base

# Copy the requirements file and install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY ./code/app.py /code/

# Set environment variables for MariaDB connection
ENV DB_HOST=127.0.0.1
ENV DB_PORT=3306
ENV DB_USER=root
ENV DB_PASSWORD=secret
ENV DB_NAME=skoly

# Define the command to run the application
CMD ["python", "app.py"]

# Use python runtime as parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /src

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libreoffice \
    unrtf \
    clamav \
    clamav-daemon \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt /app/

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Set environment variables
ENV FLASK_SECRET_KEY='the_most_secret_of_keys'
ENV FLASK_ENV=production
ENV GUNICORN_CMD_ARGS="--access-logfile - --error-logfile -"
ENV CLAMAV_UPDATE_FREQ=24
ENV LIBREOFFICE_PATH=/usr/bin/libreoffice

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for Gunicorn to find the Flask app
ENV FLASK_APP=FileConversionService:app

# Run
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

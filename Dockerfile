# Use python runtime as parent image
FROM python:3.12-bullseye

# Set the working directory in the container to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libreoffice \
    unrtf \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the src directory contents into the container at /app
COPY src/ .

# Set environment variables
ENV FLASK_SECRET_KEY='the_most_secret_of_keys'
ENV FLASK_ENV=production
ENV GUNICORN_CMD_ARGS="--access-logfile - --error-logfile -"
ENV LIBREOFFICE_PATH=/usr/bin/libreoffice

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for Gunicorn to find the Flask app
ENV FLASK_APP=main:app

# Run the Gunicorn server
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]  # Adjust this line accordingly

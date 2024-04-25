# Use python runtime as parent image
FROM python:3.12

# Set the working directory in the container to /app
WORKDIR /workdir

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libreoffice \
    unrtf \
    pandoc \
    nmon \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at the root of /workdir
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the entire project contents into the container at /workdir
COPY / . /workdir/

# Set environment variables
ENV FLASK_SECRET_KEY='the_most_secret_of_keys'
ENV FLASK_ENV=production
ENV GUNICORN_CMD_ARGS="--access-logfile - --error-logfile -"
ENV LIBREOFFICE_PATH=/usr/bin/libreoffice
ENV PYTHONPATH=/src
ENV TMPDIR /var/tmp
# Define environment variable for Gunicorn to find the Flask app
ENV FLASK_APP=app/src/app_factory.py

# Make port 5000 available to the world outside this container
EXPOSE 5000
EXPOSE 8089

# Ensure the directory exists
RUN mkdir -p $TMPDIR


# Run the Gunicorn server
CMD ["gunicorn", "-w", "18", "-b", "0.0.0.0:5000", "src.app_factory:create_app()"]

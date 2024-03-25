#Use python runtime as parent image
FROM python:3.12-slim

#Set the working directory in the container
WORKDIR /src

#copy the contents of the working directorus in the container
COPY . .

#Install dependancies listed in requirements
RUN pip install --no-cache-dir -r requirements.txt

#make port 500 available to the world outside the container
EXPOSE 5000

#Define environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

#RUN the app when the container launches
CMD ["flask", "run"]
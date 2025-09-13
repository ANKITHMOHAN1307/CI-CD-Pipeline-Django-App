#use offical Python image
FROM python:3.10-slim

#set working directory
WORKDIR /App

#Install the dependencies
COPY requirement.txt .

#copy Django project
COPY . . 

#Run the app
CMD [ "gunicorn", "--bind", "0.0.0.0:800", "app.wsi:application"]
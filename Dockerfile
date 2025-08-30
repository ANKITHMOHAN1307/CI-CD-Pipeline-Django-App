#use offical Python image
FROM python:3.10-slim

#set working directory
WORKDIR /app

#copy app code into container
COPY app.py /app

#Run the app
CMD [ "python", "app.py" ]
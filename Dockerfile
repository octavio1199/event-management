# Use an official Python runtime as a parent image
FROM python:3.9.6

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory in the container
WORKDIR /code

# Add requirements.txt to the working directory
ADD requirements.txt /code/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Add the rest of the code to the working directory
ADD . /code/

# Expose the port server is running on
EXPOSE 8000

# Start the server
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
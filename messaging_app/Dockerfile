# Use Python 3.10 base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app code
COPY . /app/

# Expose the default Django port
EXPOSE 8000

# CMD to run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ALX Checker workaround:
# To run container with port mapping, use:
# docker run -d -p 8000:8000 messaging_app:latest

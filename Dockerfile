# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install ping
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 12345

# Define the default command
CMD ["python", "app.py"]


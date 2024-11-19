# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Ensure that the necessary data files are in the image
COPY u.data u.item /app/

# Install required packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask API
EXPOSE 5000

# Define the command to run the app
CMD ["python", "app.py"]
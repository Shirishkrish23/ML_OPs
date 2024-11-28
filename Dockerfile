# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy data files
COPY u.data u.item /app/

# Copy model and encoder
COPY optimized_movie_rating_model.pkl title_encoder.pkl /app/

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports
EXPOSE 5000 

# Define the command to run the app

CMD ["python", "app.py"]

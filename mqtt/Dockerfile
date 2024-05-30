# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the MQTT script
COPY MQTT.py .

# Command to run the MQTT script and log the output
CMD ["sh", "-c", "python MQTT.py > /app/mqtt.log 2>&1"]

# Use a Python base image
FROM python:3.9

# Set the working directory
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the script
CMD ["python3", "mqtt_consumer.py"]

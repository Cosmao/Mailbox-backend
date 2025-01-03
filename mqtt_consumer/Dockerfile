# Use a Python base image
FROM python:3.9

RUN chmod 666 /certs/ca.crt /certs/mqttConsumer.crt /certs/mqttConsumer.key

# Set the working directory
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the script
CMD ["python3", "mqtt_consumer.py"]

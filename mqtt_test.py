import os
import json
import ssl
import paho.mqtt.client as mqtt
from datetime import datetime

# Environment variables
MQTT_BROKER = os.getenv("MQTT_BROKER", "pajjen.local")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "home/mailbox")  # Subscribe to all topics under "sensors/"

# Certificate paths
CA_CERT = "./certs/ca.crt"
CLIENT_CERT = "./certs/mqttConsumer.crt"
CLIENT_KEY = "./certs/mqttConsumer.key"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    current_time = datetime.now().strftime("%H:%M")
    print(f"{current_time}: Received {payload} from {msg.topic} topic")

    # Parse the JSON payload
    try:
        data = json.loads(payload)  # Convert JSON string to Python dictionary
    except json.JSONDecodeError:
        print("Failed to decode JSON")
        return


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=CA_CERT)
context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
context.check_hostname = False
client.tls_set_context(context)

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()

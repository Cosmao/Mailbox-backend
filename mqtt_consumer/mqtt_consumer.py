import os
import json
import ssl
import time
import threading
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
from discord_webhook import DiscordWebhook, DiscordEmbed
from collections import Counter

# Environment variables
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "sensors/#")  # Subscribe to all topics under "sensors/"
DISCORD_URL = os.getenv("DISCORD_URL", "")
ESP_CHECKIN_TIME_IN_HOURS = int(os.getenv("ESP_CHECKIN_TIME_IN_HOURS", 12))
ESP_STANDARD_DISTANCE_IN_MM = int(os.getenv("ESP_STANDARD_DISTANCE_IN_MM", 350))

last_msg_time = datetime.now()
last_msg_lock = threading.Lock()

if not DISCORD_URL:
    exit(1)

# Certificate paths
CA_CERT = "/certs/ca.crt"
CLIENT_CERT = "/certs/mqttConsumer.crt"
CLIENT_KEY = "/certs/mqttConsumer.key"

print(f"Starting consumer with topic `{MQTT_TOPIC}`")

def timeout_send_message():
    global last_msg_time
    while True:
        time.sleep(10)
        with last_msg_lock:
            time_diff = datetime.now() - last_msg_time

        if time_diff >= timedelta(hours=ESP_CHECKIN_TIME_IN_HOURS):
            webhook = DiscordWebhook(url=DISCORD_URL)
            embed = DiscordEmbed(title="Mailbox", description="Mailbox hasnt checked in!", color="03b2f8")
            webhook.add_embed(embed)
            response = webhook.execute()
            print(response)
            with last_msg_lock:
                last_msg_time = datetime.now()

def get_distance(data):
    most_common = Counter(data).most_common(1)[0][0]
    return most_common

def decode_message(data):
    desc = ""
    if "lid" in data:
        value = data.get("lid")
        if value == "open":
            desc += "Lid is open!"

    if "distance" in data:
        value = get_distance(data["distance"])
        if ESP_STANDARD_DISTANCE_IN_MM * 0.95 <= value <= ESP_STANDARD_DISTANCE_IN_MM * 1.05:
            desc += "Probably not letter inside!\nDist: `{}`".format(value)
        else:
            desc += "Most likely letter inside!\nDist: `{}`".format(value)

    if desc:
        webhook = DiscordWebhook(url=DISCORD_URL)
        embed = DiscordEmbed(title="Mailbox", description=desc)
        webhook.add_embed(embed)
        response = webhook.execute()
        print(response)

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global last_msg_time
    with last_msg_lock:
        last_msg_time = datetime.now()
    payload = msg.payload.decode()
    print(f"Received `{payload}` from `{msg.topic}` topic")
    # Parse the JSON payload
    try:
        data = json.loads(payload)  # Convert JSON string to Python dictionary
        decode_message(data)
    except json.JSONDecodeError:
        print("Failed to decode JSON")
    return

thread = threading.Thread(target=timeout_send_message)
thread.start()

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

# Mailbox-backend
Backend for [ESP-Mailbox](https://github.com/Cosmao/ESP-Mailbox).
## Setup
### Certificates
Generate certificates with `keygen.sh` or with your preferred means and put them inside the `certs/` directory. The expected names are as follows:
| Name | Use |
| ------ | ------ |
| ca.crt | The certificate authority |
| server.key | Servers RSA key |
| mqttConsumer.key | The mqtt-consumers key to access the mqtt broker |
| mqttConsumer.crt | The mqtt-consumers certificate |

The keygen script will also generate a key and certificate pair for the ESP32 unit.
### Configuration
The `docker-compose.yml` file contains enviroment variables you can use for configuring the project.
| Variable | Description|
| ------ | ------ |
| MQTT_TOPIC | What topic the mqtt consumer is supposed to listen to |
| DISCORD_URL | The webhook URL the mqtt consumer is supposed to send messages to |
| ESP_CHECKIN_TIME_IN_HOURS | After how many hours its supposed to send an alert that the ESP hasnt checked in |
| MQTT_PORT | If you want to connect to a different port, also need to change the port in the mailbox-mosquitto service |
### Starting
Simply start the project up with docker-compose and it should handle the rest. Theres a provided testscript called `mqtt_test.py` in the root directory that will attempt to connect to the broker and print out everything sent on the topic.

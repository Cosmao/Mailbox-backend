if [ ! -d certs ]; then
  mkdir -p certs
fi

cd certs

# Generate server key
openssl genrsa -out server.key 2048

# Generate CA certificate with country and organization
openssl req -new -x509 -days 3650 -key server.key -out ca.crt -subj "/C=SE/O=iot23/CN=localhost"

# Generate esp32 and consumer key
openssl genrsa -out esp32.key 2048
openssl genrsa -out mqttConsumer.key 2048

# Create esp32 and consumer certificate signing request with country and organization
openssl req -new -key esp32.key -out esp32.csr -subj "/C=SE/O=iot23/CN=localhost"
openssl req -new -key mqttConsumer.key -out mqttConsumer.csr -subj "/C=SE/O=iot23/CN=localhost"

# Sign the esp32 and consumer certificate with the CA certificate
openssl x509 -req -in esp32.csr -CA ca.crt -CAkey server.key -CAcreateserial -out esp32.crt -days 3650
openssl x509 -req -in mqttConsumer.csr -CA ca.crt -CAkey server.key -CAcreateserial -out mqttConsumer.crt -days 3650

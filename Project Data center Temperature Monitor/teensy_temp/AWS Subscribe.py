import paho.mqtt.client as mqtt

# Configure the MQTT broker and topic
mqtt_broker = "52.64.221.225"
mqtt_port = 1883
mqtt_topic = "temperature_data"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, message):
    # Callback when a message is received from Teensy
    data = message.payload.decode()
    print(f'Received data: {data}')
    # You can process the received data as needed

# Configure the MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the MQTT broker
mqtt_client.connect(mqtt_broker, mqtt_port, 60)

# Start the MQTT client loop to receive data
mqtt_client.loop_forever()
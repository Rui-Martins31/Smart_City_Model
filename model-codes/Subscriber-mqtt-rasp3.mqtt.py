import paho.mqtt.client as mqtt

# --- MQTT Configuration ---
broker_address = "192.168.0.106"  # IP address of your Raspberry Pi 5 (broker)
broker_port = 1883                # MQTT port (default is 1883)
mqtt_topic = "detection/events"    # Topic to subscribe to

# Define callback function to handle incoming messages
def on_message(client, userdata, msg):
    print(f"Message received: {msg.payload.decode()}")

# Create an MQTT client instance
mqtt_client = mqtt.Client("RaspberryPi3BClient")

# Assign the callback function for messages
mqtt_client.on_message = on_message

# Connect to the MQTT broker
mqtt_client.connect(broker_address, broker_port, keepalive=60)

# Subscribe to the topic
mqtt_client.subscribe(mqtt_topic)

# Start the MQTT loop to receive messages
mqtt_client.loop_forever()
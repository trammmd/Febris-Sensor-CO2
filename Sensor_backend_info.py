from __future__ import print_function
import paho.mqtt.client as mqtt
import json
import ssl

# Create a new MQTT client instance
client = mqtt.Client()

# MQTT broker address and port
broker_address = "mioty-server-1.iis.fraunhofer.de"
broker_port = 8883
    
# MQTT credentials
username = "stud"       
password = "mioty$stud"       

# Set the username and password (
if username is not None and password is not None:
    client.username_pw_set(username, password)

# MQTT topic to subscribe to
topic = "mioty/70-b3-d5-67-70-0e-ff-03/fc-a8-4a-03-00-00-0e-67/uplink"
qos_level = 2


# Path to the client certificate and key files 
cert_file = None
key_file = None

# Create an SSL context and load the client certificate and key files
ssl_context = ssl.create_default_context()
if cert_file is not None and key_file is not None:
    ssl_context.load_cert_chain(cert_file, key_file)  
    
# Set the SSL context for secure connection
client.tls_set_context(context=ssl_context)


# Connect to the MQTT broker
if client.connect(broker_address, broker_port) != 0:
    print("Could not connect to MQTT broker!")
    SystemExit(-1)
    
receivedMessage = ""

# Callback function that will be called when a new message is received
def on_message(client, userdata, message):
    # new mioty telegram received
    print("Received Topic: " + message.topic)
    # print message as json
    #print("Received Message: " + message.payload)
    receivedMessage = str(message.payload.decode())
    print("Received message: " + receivedMessage)

# Set the callback function for new messages
client.on_message = on_message

# Subscribe to the topic
client.subscribe(topic, qos=qos_level)

# Publish a message to the topic with QoS 1
#client.publish(publish_topic, receivedMessage, qos=qos_level)

# Start the MQTT client loop to listen for new messages
try:
    print("Press CTRL+C to exit")
    client.loop_forever()
except  KeyboardInterrupt: 
    client.loop_stop() 
    client.disconnect()
 
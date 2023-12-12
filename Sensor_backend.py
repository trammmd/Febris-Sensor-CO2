from __future__ import print_function
import paho.mqtt.client as mqtt
import json
import ssl

# mqtt configuration
adresse = "mioty-server-1.iis.fraunhofer.de"
port = 8883
qos_level = 2
topic = 'mioty/70-b3-d5-67-70-0e-ff-03/fc-a8-4a-03-00-00-0e-67/uplink'

# MQTT credentials
username = "stud"       
password = "mioty$stud"  

#callback function to receive messages from broker
# Called when a message has been received on a topic that the client subscribed to without specific topic filter
def on_message(client, userdata, message):
    # new mioty telegram received and print topic
    print("received topic:", message.topic) 
    #print message as Json String 
    receivedMessage = str(message.payload.decode())
    print("Received message: " + receivedMessage)


# callback function, called when broker responds to connection request
def on_connect(client,userdata,flag,rc): 
    print("connected")
    client.subscribe(topic, qos=2) #subscribe to topic)   
     

# debugging function
def on_log(client, userdata, level, buf):
    print("log: ",buf)

def user_identify(client, username, password):
    # Path to the client certificate and key files 
    cert_file = None
    key_file = None
    # Create an SSL context and load the client certificate and key files
    ssl_context = ssl.create_default_context()
    # Set the username and password
    if username is not None and password is not None:
        client.username_pw_set(username, password)
    if cert_file is not None and key_file is not None:
        ssl_context.load_cert_chain(cert_file, key_file)  
    #Set the SSL context for secure connection
    client.tls_set_context(context=ssl_context)

# creates new client object 
client = mqtt.Client()   
client.user_identify = user_identify
# functions get assigned to the actual callbacks
client.on_connect = on_connect
client.on_message = on_message   

# Subscribe to the topic
client.subscribe(topic, qos=qos_level)    

# connects client to broker
client.connect(adresse, port) 

# Start the MQTT client loop to listen for new messages
try:
    print("Press CTRL+C to exit")
    client.loop_forever()
except  KeyboardInterrupt: 
    client.loop_stop() 
    client.disconnect()
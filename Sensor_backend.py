# allows to use features from possibly higher Python versions by backporting them into the current interpreter
from __future__ import print_function
# imports client class, necessary for important paho functions and features 
import paho.mqtt.client as mqtt
# if required, further security functions such as encryption of the connection or identity verification can be added
import ssl
# allows among other things to decode Jason coded strings
import json

# mqtt configuration
server = "mioty-server-1.iis.fraunhofer.de"
port = 8883
topic = 'mioty/70-b3-d5-67-70-0e-ff-03/fc-a8-4a-03-00-00-0e-67/uplink'
#topic schemes: devices/<customerTransformedName>/<deviceBaseType>/<deviceType>/<deviceId>/up

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
    # sets username and password
    client.username_pw_set(username, password)
    # Path to the client certificate and key files 
    cert_file = None
    key_file = None
    # Create an SSL context and load the client certificate and key files
    ssl_context = ssl.create_default_context()
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

# connects client to broker
client.connect(server, port) 

try:
    client.loop_forever()
except KeyboardInterrupt: 
    client.loop_stop() 
    client.disconnect()
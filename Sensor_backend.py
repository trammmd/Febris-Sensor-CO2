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
topic = 'devices/stud/febris/+/FC-A8-4A-03-00-00-0E-66/alarmstatus'
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
    print(" ", message.payload) 
    

# callback function, called when broker responds to connection request
def on_connect(client,userdata,flag,rc): 
    client.subscribe(topic, qos=2)    
    print("connect")
         

# debugging function
def on_log(client, userdata, level, buf):
    print("log: ",buf)
    
# creates new client object
client = mqtt.Client("mioty")
# sets username and password
client.username_pw_set(username, password)
# functions get assigned to the actual callbacks
client.on_connect = on_connect
# miotyClient.on_log = on_log
client.on_message = on_message
# connects client to broker
client.connect(server, port, 60) 

try:
    client.loop_forever()
except KeyboardInterrupt: 
    client.loop_stop() 
    client.disconnect()
from __future__ import print_function
import paho.mqtt.client as mqtt
import json
import ssl
import mysql.connector

# Create a new MQTT client instance
client = mqtt.Client()

# MQTT broker address and port
broker_address = "broker_address"
broker_port = 8883
    
# MQTT credentials
username = "username"       
password = "password"       

# Set the username and password 
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

# Function to filter the data, which will be saved it to database
def filter(data):
    # Dictionary to store the filtered data
    filtered_data = {}

    # Check if 'components' key exists and contains relevant data
    if 'components' in data:
        for component in data['components']:
            if 'alarm' in component.lower() or 'temp' in component.lower() or 'humid' in component.lower() or 'co2' in component.lower() or 'pressure' in component.lower() or 'battery' in component.lower():
                filtered_data[component] = data['components'][component]

    return filtered_data

# Callback function that will be called when a new message is received
def on_message(client, userdata, message):
    mydb = None
    mycursor = None
    try:
        # Message payload as JSON string
        receivedMessage_json = json.loads(message.payload.decode("utf-8"))

        # Extract individual components from the received JSON
        alarm = json.dumps(receivedMessage_json.get("alarm", {}))
        temperature = json.dumps(receivedMessage_json.get("temperature", {}))
        humidity = json.dumps(receivedMessage_json.get("humidity", {}))
        co2 = json.dumps(receivedMessage_json.get("co2", {}))
        pressure = json.dumps(receivedMessage_json.get("pressure", {}))
        battery = json.dumps(receivedMessage_json.get("battery", {}))

        # Connect to the MySQL database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="sensors_db"
        )

        mycursor = mydb.cursor()

        # Insert data into the data_log table
        sql = """INSERT INTO data_log (sensor, alarm, temperature, humidity, co2, pressure, battery) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        val = (1, alarm, temperature, humidity, co2, pressure, battery) # Assuming '1' is your sensor ID
        mycursor.execute(sql, val)

        # Commit the changes to the database
        mydb.commit()
    # Handle exceptions and close connections 
    except json.JSONDecodeError:
        print("Error decoding JSON from the message payload.")
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()

# Set the callback function for new messages
client.on_message = on_message

# Subscribe to the topic
client.subscribe(topic, qos=qos_level)

# Start the MQTT client loop to listen for new messages
try:
    print("Press CTRL+C to exit")
    client.loop_forever()
except  KeyboardInterrupt: 
    client.loop_stop() 
    client.disconnect()
 
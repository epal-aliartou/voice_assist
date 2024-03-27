# https://www.youtube.com/watch?v=Q0S0xOW35k8&t=266s&ab_channel=ResinChemTech
# https://www.youtube.com/watch?v=9N6a-VLBa2I&t=212s&ab_channel=CoreySchafer
import time
import paho.mqtt.client as paho
from paho import mqtt
import csv

def on_connect(client, userdata, flags, rc, properties=None):# setting callbacks for different events to see if it works, print the message etc.
    print("CONNACK received with code %s." % rc)

def on_publish(client, userdata, mid, properties=None):# with this callback you can see if your publish was successful
    print("mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):# print which topic was subscribed to
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# def on_message(client, userdata, msg): # print message, useful for checking if it was successful
#     print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
#     print(type(msg.payload))
#     # print(b'Easy \xE2\x9C\x85'.decode("utf-8"))
#     print(msg.payload.decode('UTF-8'))

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5) # using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31  # userdata is user defined data of any type, updated by user_data_set()  # client_id is the given name of the client
client.on_connect = on_connect

# client.username_pw_set("mqtt_user", "mqtt_user1234")# enable TLS for secure connection# client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)# set username and password
# client.connect("192.168.1.78", 1883)# connect to HiveMQ Cloud on port 8883 (default for MQTT)

client.on_subscribe = on_subscribe # setting callbacks, use separate functions like above for better visibility
# client.on_message = on_message
client.on_publish = on_publish

# client.subscribe("encyclopedia/#", qos=1)# subscribe to all topics of encyclopedia by using the wildcard "#"
# client.publish("encyclopedia/temperature", payload="mqtt_neo", qos=1)# a single publish, this can also be done in loops, etc.

# client.loop_forever()# loop_forever for simplicity, here you need to stop the loop manually# you can also use loop_start and loop_stop

import paho.mqtt.client as mqtt 
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("sensor/bluetooth/#") #subscribes to particular topic

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    localtime = time.asctime( time.localtime(time.time()) )
    with open('data.txt','a') as f:
        f.write("[" + localtime + "] ")
        f.write("[" + msg.topic + "] ")
        f.write(str(msg.payload.decode("utf-8"))+"\n")

client = mqtt.Client()
client.on_connect = on_connect 
client.on_message = on_message 

print("Connecting")
client.connect("localhost", 1883, 60) 
client.loop_forever() 


print(client.subscribe([("sensor/bluetooth/temp",0),("sensor/bluetooth/pressure",0),("sensor/bluetooth/accelerometer",0)]))
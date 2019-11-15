import paho.mqtt.client as mqtt
import numpy as np
import json
import os
import cv2
import numpy as np
from keras.models import model_from_json
from keras.preprocessing import image
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

# ignore warnings
import warnings
warnings.filterwarnings("ignore")

emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
img_data = np.zeros(shape=(5,2))

def load_model():
    global model
    #load model
    model = model_from_json(open("fer.json", "r").read())
    #load weights
    model.load_weights('fer.h5')

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to broker.")
        client.subscribe("Group_2/IMAGE/classify")
    else:
        print("Connection failed with code")

def classify_emotion(data):
    print(data)
    print("Start classifying")
    predictions = model2.predict(data)
    print(predictions)
    win= np.argmax(predictions[0])
    print(win)
    print("Done.")
    return {"prediction": emotions[win]}

def on_message(client, userdata, msg):
    recv_dict = json.loads(msg.payload)
    print(recv_dict["timestamp"])
    print("\n")
    img_data = np.array(recv_dict["data"])
    result = classify_emotion(img_data)
    print("results: ", result)

def setup(hostname):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(hostname)
    client.loop_start()
    return client

def main():
    load_model()
    setup("localhost")
    while True:
        pass

if __name__ == '__main__':
    main()

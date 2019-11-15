import os
import paho.mqtt.client as mqtt
import numpy as np
from PIL import Image
import json
import cv2
import numpy as np
from keras.models import model_from_json
from keras.preprocessing import image
import time

# ignore warnings
import warnings
warnings.filterwarnings("ignore")

face_haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


cap=cv2.VideoCapture(0)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected.")
        client.subscribe("Group_2/IMAGE/predict")
    else:
        print(("Failed to connect. Error code: %d." % rc))

def on_message(client, userdata, msg):
    print("Received message from server.")
    resp_dict = json.loads(msg.payload)
    print((("Prediction: %s") % ( resp_dict["prediction"])))

def setup(hostname):
    client = mqtt.Client()
    client.on_connect = on_connect
    #client.on_message = on_message
    client.connect(hostname)
    client.loop_start()
    return client

def main():
    client = setup("localhost")
    start_time_st = time.time()
    start_time = time.time()
    while True:
        ret,test_img=cap.read()# captures frame and returns boolean value and captured image
        if not ret:
            continue
        gray_img= cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
        if time.time() - start_time >= 2:
            faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)
            for (x,y,w,h) in faces_detected:
                print('face detected\n')
                cv2.rectangle(test_img,(x,y),(x+w,y+h),(255,0,0),thickness=7)
                roi_gray=gray_img[y:y+w,x:x+h]#cropping region of interest i.e. face area from  image
                roi_gray=cv2.resize(roi_gray,(48,48))
                img_pixels = image.img_to_array(roi_gray)
                img_pixels = np.expand_dims(img_pixels, axis = 0)
                img_pixels /= 255
                img=img_pixels
                img=img.tolist()
                print("Sending data.")
                send_dict = {"data":img,"timestamp":time.time()-start_time_st}
                client.publish("Group_2/IMAGE/classify", json.dumps(send_dict))
            start_time = time.time()
if __name__ == '__main__':
    main()

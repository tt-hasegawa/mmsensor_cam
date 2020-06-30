import base64
import cv2
import datetime
import numpy as np
import os
import picamera
import requests
import sys
import time
import logging
from PIL import Image
from yolo import YOLO, detect_video
from yolo2 import YOLO2

logging.basicConfig(filename='/tmp/sensor-popluation.log', level=logging.DEBUG)

url='http://192.168.46.128:3000'
#proxies = {
#    'http': 'http://proxy:12080',
#    'https': 'http://proxy:12080'
#}
proxies = {
    'http': None,
    'https': None
}

logging.info("PopulationSensor Start.[{}]".format(url))

# Initialize Camera
camera = picamera.PiCamera()
time.sleep(2)

# analyze picture by AI
yolo = YOLO()
yolo2 = YOLO2()

logging.info("PopulationSensor Initialized.")

while True:
    logging.info("Check Start.")

    camera.capture('tmp.jpg')
    image = Image.open('tmp.jpg')
    result = yolo2.detect_image(image)
    r_image=yolo.detect_image(image)
    cv2.imwrite("out.jpg",np.asarray(r_image)[...,::-1])
    
    person=0
    for r in result:
        if r[0].startswith('person'):
            print(r[0])
            person+=1
    logging.info("Check Camera People:{}.".format(person))

    uploadData={
            'population':str(person)
    }
    logging.info(uploadData)
    try:
        with open('out.jpg', 'rb') as f:
            data = f.read()
            uploadData['image']=base64.b64encode(data).decode('utf-8')
            logging.info("POST Start.{}")
            response = requests.post(url + '/addPopulation/' , json=uploadData, proxies=proxies)
            logging.info("POST End. {}".format(response.text))
    except Exception as e:
        logging.info(e)
    time.sleep(10)


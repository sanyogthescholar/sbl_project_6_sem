import numpy as np
import matplotlib.pyplot as plt
import requests as req
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from matplotlib import patches
from PIL import Image
from flask import Flask, render_template, request
import cv2
import base64
import os

app = Flask(__name__)

ENDPOINT = "https://sbl-face-api.cognitiveservices.azure.com/"
SUBSCRIPTION_KEY = os.environ["SUBSCRIPTION_KEY"]
FACE_API_URL = "https://sbl-face-api.cognitiveservices.azure.com/" + "/face/v1.0/detect"

headers = {
    'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
    'Content-Type': 'application/octet-stream'
}

params = {
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'true',
    'returnFaceAttributes': 'age,gender,glasses,smile'
}


def data_uri_to_cv2_img():
  encoded_data = request.values['imagebase64']
  encoded_data = encoded_data.split(',')[1]
  nparr = np.fromstring(encoded_data.decode('base64'), np.uint8)
  img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
  return img

def readb64():
  print("In start of readb64")
  encoded_data = request.values['base64data']
  encoded_data = encoded_data.split(',')[1]
  nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
  img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
  print("cv2.imdecode done")
  cv2.imwrite( './temp.jpg', img)
  print("imwrite done")
  return "./temp.jpg"

# Load Image
#image_filepath = "C:/Users/Aayusha/Desktop/withoutmask.png"
#pil_image = Image.open(image_filepath, 'r')


def call_face_api(image_filepath):
    print("cfa 53")
    params = {
        'returnFaceId': 'false',
        'returnFaceLandmarks': 'true',
        'returnFaceAttributes': 'mask',
        'detectionModel': 'detection_03'
    }
    print("cfa 60")
    image_data = open(image_filepath, 'rb').read()
    print("cfa 62")
    session = req.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.post(
        FACE_API_URL,
        params=params,
        headers=headers,
        data=image_data,
        verify=False
    )
    print("cfa 69")
    response_data = response.json()
    return response_data

def plot_image_with_mask_label(image_filepath):
    print("start of piwml")
    print(image_filepath)
    response_data = call_face_api(image_filepath)
    print("73 done")
    pil_image = Image.open(image_filepath, 'r')
    print("75 done")
    plt.figure(figsize=(15, 7))
    plt.imshow(pil_image)
    print("78 done")
    pil_image.save("./img-1.png")
    print("81 done")
    print(response_data)
    for detected_face in response_data:
        rectangle_data =  detected_face['faceRectangle']
        x = rectangle_data['left']
        y = rectangle_data['top']
        w = rectangle_data['width']
        h = rectangle_data['height']
        if detected_face['faceAttributes']['mask']['type'] == 'noMask':
            label_str = "No Mask"
            color_str = "red"
        else:
            label_str = "Wearing Mask"
            color_str = "limegreen"
        rect = patches.Rectangle([x, y], w, h,linewidth=2, edgecolor=color_str, facecolor='none')
        ax = plt.gca()
        plt.text(x,y + h + 60,label_str,size=15,c=color_str)
        ax.add_patch(rect)
        #plt.show()
        plt.tight_layout()
        plt.savefig("./static/img-2.jpg")

def verify(img):
  print("verify started")
  plot_image_with_mask_label(img)
  print("verify over")

@app.route('/')
#@cross_origin()
def upload_form():
  print("SERVER STARTED")
  return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def get_student_image():
  img_ret = readb64()
  print("img_ret done")
  verify(img_ret) #where the magic happens
  return render_template("done.html")

#app.run(port=5000, debug=True)
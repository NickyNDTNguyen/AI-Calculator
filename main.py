import base64
import re
import numpy as np
import cv2
import mahotas
import imutils
import tensorflow as tf
from flask import Flask, render_template, request
from blueprints import *

app = Flask(__name__)

app.register_blueprint(homepage)
app.register_blueprint(camera_page)

model = tf.keras.models.load_model("static/cnn_math_v1.h5")

# img_height = 192
# img_width = 192
# channels = 3
label_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'addition', 'division', 'multiplication', 'subtraction']

@app.route("/")
def landing_page():
    return render_template("index.html")

def parse_image(imgData):
    imgstr = re.search(b"base64,(.*)", imgData).group(1)
    img_decode = base64.decodebytes(imgstr)
    with open("output.jpg", "wb") as file:
        file.write(img_decode)
    return img_decode

def deskew(image, width):
    (h, w) = image.shape[:2]
    moments = cv2.moments(image)

    skew = moments['mu11'] / moments['mu02']
    M = np.float32([[1, skew, -0.5*w*skew],
                    [0, 1, 0]])
    image = cv2.warpAffine(image, M, (w, h), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)

    image = imutils.resize(image, width=width)

    return image

def center_extent(image, size):
    (eW, eH) = size

    if image.shape[1] > image.shape[0]:
        image = imutils.resize(image, width=eW)
    else:
        image = imutils.resize(image, height=eH)

    extent = np.zeros((eH, eW), dtype='uint8')
    offsetX = (eW - image.shape[1]) // 2
    offsetY = (eH - image.shape[0]) // 2
    extent[offsetY:offsetY + image.shape[0], offsetX:offsetX+image.shape[1]] = image

    CM = mahotas.center_of_mass(extent)
    (cY, cX) = np.round(CM).astype("int32")
    (dX, dY) = ((size[0]//2) - cX, (size[1] // 2) - cY)
    M = np.float32([[1, 0, dX], [0, 1, dY]])
    extent = cv2.warpAffine(extent, M, size)

    return extent


@app.route("/upload/", methods=["POST"])
def upload_file():
    img_raw = parse_image(request.get_data())
    nparr = np.fromstring(img_raw, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = (np.float32(image), cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    edged = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in  cnts], key=lambda x: x[1])
    ###
    math_detect = []
    for (c, _) in cnts:
        (x, y, w, h) = cv2.boundingRect(c)

        if w >=7 and h>=20:
            roi = edged[y:y+int(1.2*h), x:x+w]
            thresh = roi.copy()

            thresh = deskew(thresh, 28)
            thresh = center_extent(thresh, (28, 28))
            thresh = np.reshape(thresh, (28, 28, 1))
            thresh = thresh / 255
            predictions = model.predict(np.expand_dims(thresh, axis=0))
            digit = np.argmax(predictions[0])
            print(predictions[0])

            cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(image, label_names[digit], (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)
            math_detect.append(label_names[digit])

    def convert_math(math_detect):
        for i in range(0, len(math_detect)):
            if math_detect[i] == 'addition':
                math_detect[i] = '+'
            elif math_detect[i] == 'division':
                math_detect[i] = '/'
            elif math_detect[i] == 'multiplication':
                math_detect[i] = '*'
            elif math_detect[i] == 'subtraction':
                math_detect[i] = '-'
        return math_detect
    
    def calculate_string(math_detect):
        math_detect = convert_math(math_detect)
        calculator = ''.join(str(item) for item in math_detect)
        result = (calculator + ' = ' + str(eval(calculator)))
        return result

    result = calculate_string(math_detect)

    return result

if __name__ == '__main__':
    app.run(debug=True)
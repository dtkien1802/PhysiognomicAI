import pickle
from typing import Sequence
from flask import Flask, render_template, request,jsonify
import dlib
from mtcnn.mtcnn import MTCNN
from random import random
import cv2
from imutils import face_utils
import base64
import numpy as np
import os

app = Flask(__name__, template_folder="../../frontend")
app.config['UPLOAD_FOLDER'] = "static"

filename = '../models/model.sav'
clf = pickle.load(open(filename, 'rb'))

desc_file = "../models/face_desc.csv"
f = open(desc_file, "r", encoding="utf8")
desc = f.readlines()
f.close()
dict = {}
for line in desc:
    dict[line.split('|')[0]] = [line.split('|')[1], line.split('|')[2]]

detector = MTCNN()
predictor = dlib.shape_predictor(
    "../models/shape_predictor_68_face_landmarks.dat")

@app.route("/", methods=['GET'])
def home_page():
    return render_template('index.html')

@app.route("/about", methods=['GET'])
def about_page():
    return render_template('about.html', team_image="a.jpg")

cnt=1
@app.route('/', methods=['POST'])
def AI():
    try:
        global cnt
        img_base64 = request.form["img"]
        path_to_save='image/img'+str(cnt)+'.jpg'
        cnt=cnt+1
        img_binary = base64.b64decode(img_base64)
        img_jpg=np.frombuffer(img_binary, dtype=np.uint8)
        img = cv2.imdecode(img_jpg, cv2.IMREAD_COLOR)
        cv2.imwrite(path_to_save, img)
        frame = cv2.imread(path_to_save)
        os.remove(path_to_save)
        results = detector.detect_faces(frame)

        if len(results) != 0:
            for result in results:
                x1, y1, width, height = result['box']
                x1, y1 = abs(x1), abs(y1)
                x2, y2 = x1 + width, y1 + height
                face = frame[y1:y2, x1:x2]
                landmark = predictor(
                    frame, dlib.rectangle(x1, y1, x2, y2))
                landmark = face_utils.shape_to_np(landmark)
                landmark = landmark.reshape(68 * 2)

                y_pred = clf.predict([landmark])
                extra = dict[y_pred[0]][1]
                ID = dict[y_pred[0]][0]

                # cv2.imwrite(path_to_save, face)
                break

            return jsonify(
                msg="Gửi ảnh lên server lên thành công",
                extra=extra,
                face_shape=ID
            )
        else:
            return jsonify( msg="Không nhận diện được khuôn mặt")
    except Exception as ex:
        return jsonify( msg="Không nhận diện được khuôn mặt")

if __name__ == '__main__':
    app.run(debug=True)

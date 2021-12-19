import os
import cv2
from mtcnn import MTCNN
import dlib
from imutils import face_utils
import pickle
import numpy as np

detector=MTCNN()
landmark_detector=dlib.shape_predictor("../models/shape_predictor_68_face_landmarks.dat")
data_folder="../face_data"

landmark_list=[]
label_list=[]

for label in os.listdir(data_folder):
    if '.' in label:
        continue
    cnt=0
    path_label=os.path.join(data_folder,label)
    for file_name in os.listdir(path_label):
        if cnt>=200:
            break
        path_file=os.path.join(path_label,file_name)
        image=cv2.imread(path_file)
        if image is None:
            continue
        results=detector.detect_faces(image)
        if len(results)>0:
            result = results[0]

            x1, y1, width, height = result['box']
            x2 = x1 + width
            y2 = y1 + height

            landmark=landmark_detector(image,dlib.rectangle(x1,y1,x2,y2))
            landmark=face_utils.shape_to_np(landmark)
            landmark=landmark.reshape(68*2)
            landmark_list.append(landmark)
            label_list.append(label)
            cnt+=1

            
print(len(landmark_list))
landmark_list=np.array(landmark_list)
lable_list=np.array(label_list)

file=open("../models/landmarks.pkl",'wb')
pickle.dump(landmark_list,file)
file.close()

file=open("../models/labels.pkl",'wb')
pickle.dump(label_list,file)
file.close()
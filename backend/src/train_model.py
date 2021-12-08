import pickle
from sklearn import svm
file=open("../models/landmarks.pkl",'rb')
landmark_list=pickle.load(file)
file.close()

file=open("../models/labels.pkl",'rb')
label_list=pickle.load(file)
file.close()

print(len(label_list))

model=svm.SVC(kernel="linear")
model.fit(landmark_list,label_list)

file=open("../models/model.sav",'wb')
pickle.dump(model,file)
file.close()
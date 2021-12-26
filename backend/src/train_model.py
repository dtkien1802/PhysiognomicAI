import pickle
from sklearn.svm import SVC
file=open("../models/landmarks.pkl",'rb')
landmark_list=pickle.load(file)
file.close()

file=open("../models/labels.pkl",'rb')
label_list=pickle.load(file)
file.close()

print("total samples :",len(landmark_list))

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(landmark_list,label_list, test_size=0.2, random_state=1)

print("number of training samples :",len(X_train))
print("number of test samples :",len(X_test))

model=SVC(kernel='linear',C=0.001)
model.fit(X_train,y_train)

y_pred=model.predict(X_test)

from sklearn.metrics import accuracy_score,precision_score,confusion_matrix
matrix = confusion_matrix(y_test, y_pred)
print(matrix)
print("Accuracy score for each class: ",matrix.diagonal()/matrix.sum(axis=1))
print('Accuracy score - Test dataset: {}'.format(accuracy_score(y_test, y_pred)))

print('Precision_score - Test dataset: {}'.format(precision_score(y_test, y_pred,average=None)))

file=open("../models/model.sav",'wb')
pickle.dump(model,file)
file.close()
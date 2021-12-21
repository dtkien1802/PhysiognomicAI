import pickle
from sklearn import svm
file=open("../models/landmarks.pkl",'rb')
landmark_list=pickle.load(file)
file.close()

file=open("../models/labels.pkl",'rb')
label_list=pickle.load(file)
file.close()

print(len(label_list))

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(landmark_list,label_list, test_size=0.1, random_state=1)

model=svm.SVC(kernel="linear")
model.fit(X_train,y_train)

y_pred=model.predict(X_test)

from sklearn.metrics import accuracy_score
print('Accuracy score - Test dataset: {}'.format(accuracy_score(y_test, y_pred)))


file=open("../models/model.sav",'wb')
pickle.dump(model,file)
file.close()
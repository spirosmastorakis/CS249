import csv
import random
from sklearn import svm

from sklearn.ensemble import  RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

def load_train_data(filename):
    label = []
    data = []
    avg = list()
    num = list()
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append([float(row[i]) for i in range(0, len(row) - 1)])
            label.append(int((int(row[-1]) + 1) / 2))
            if len(avg) == 0:
                avg = [0.0] * (len(row) - 1)
                num = [0] * (len(row) - 1)

            for i in range(0, len(row) - 1):
                if float(row[i]) >= 0:
                    avg[i] += float(row[i])
                    num[i] += 1

    for i in range(0, len(avg)):
        if num[i] > 0:
            avg[i] = avg[i] / float(num[i])
    for feature in data:
        for i in range(0, len(avg)):
            if feature[i] < 0:
                feature[i] = avg[i]
    print(avg)
    return data, label

def predict(clf, training_data, training_label, testing_data, testing_label):
    predict_label = clf.predict(training_data)
    err_count = 0
    for i in range(len(training_label)):
        if predict_label[i] != training_label[i]:
            err_count += 1
    print("train err: ", err_count, "/", len(training_label), ' is ', float(err_count) / len(training_label))


    predict_label = clf.predict(testing_data)
    err_count = 0
    for i in range(len(testing_label)):
        if predict_label[i] != testing_label[i]:
            err_count += 1
    print("over all err: ", err_count, "/", len(testing_label), ' is ', float(err_count) / len(testing_label))


def learning_svm(training_data, training_label, testing_data, testing_label):

    # sample = range(5000)

    clf = svm.LinearSVC(C = 2.0)
    clf.fit(training_data, training_label)
    print(clf)

    predict(clf, training_data, training_label, testing_data, testing_label)
    

def learning_randomforest(training_data, training_label, testing_data, testing_label):
    clf = RandomForestClassifier(n_estimators=1000,verbose=2,n_jobs=10,min_samples_split=10,random_state=1,criterion='gini',compute_importances='True')
    clf = clf.fit(training_data, training_label)

    predict(clf, training_data, training_label, testing_data, testing_label)


if __name__ == "__main__":    
    data, label = load_train_data("features_train_3.csv")
    print("load train data done...")
    print(len(data))

    sample = random.sample(range(len(data)), 10000)

    training_data = [data[i] for i in sample]
    training_label = [label[i] for i in sample]

    # learning_svm(training_data, training_label, data, label)
    learning_randomforest(training_data, training_label, data, label)


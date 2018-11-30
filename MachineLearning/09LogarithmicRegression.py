# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 10:39:22 2018

@author: Cristina
"""

import pandas as pd
import pylab as pl
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt

churn_df = pd.read_csv("ChurnData.csv")
churn_df.head()

#Preprocessing and selection
churn_df = churn_df[["tenure", "age", "address", "income", "ed", "employ", "equip", "callcard", "wireless", "churn"]]
churn_df["churn"] = churn_df["churn"].astype("int")
churn_df.head()

churn_df.shape

X = np.asarray(churn_df[["tenure", "age", "address", "income", "ed", "employ", "equip", "callcard", "wireless"]])
X[0:5]

y= np.asarray(churn_df["churn"])
y[0:5]

#normalise data
from sklearn import preprocessing
X = preprocessing.StandardScaler().fit(X).transform(X)
X[0:5]


#Train/test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)
print ('Train set:', X_train.shape,  y_train.shape)
print ('Test set:', X_test.shape,  y_test.shape)


#Modelling logistic regression with scikit-learn
"""
The version of Logistic Regression in Scikit-learn, support regularization. 
Regularization is a technique used to solve the overfitting problem in machine 
learning models. C__ parameter indicates __inverse of regularization strength 
which must be a positive float. Smaller values specify stronger regularization.
"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
LR = LogisticRegression(C=0.01, solver="liblinear").fit(X_train, y_train)
LR

yhat = LR.predict(X_test)
yhat

"""
predict_proba returns estimates for all classes, ordered by the label of classes. 
So, the first column is the probability of class 1, P(Y=1|X), and second column 
is probability of class 0, P(Y=0|X)
"""
yhat_prob = LR.predict_proba(X_test)
yhat_prob


#Evaluation
#Jaccard index (size of the intersection divided by the size of the union of two label sets)
from sklearn.metrics import jaccard_similarity_score
jaccard_similarity_score(y_test, yhat)

#Confusion matrix
from sklearn.metrics import classification_report, confusion_matrix
import itertools
def plot_confusion_matrix(cm, classes, normalise=False, title="Confusion matrix",
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalisation can be applied by setting normalise=True.
    """
    if normalise:
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
        print("Normalised confusion matrix")
    else:
        print("Confusion matrix, without normalization")

    print(cm)

    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = ".2f" if normalise else "d"
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel("True label")
    plt.xlabel("Predicted label")
    
#Compute confusion matrix
cnf_matrix = confusion_matrix(y_test, yhat, labels=[1,0])
np.set_printoptions(precision=2)
cnf_matrix

#Plot confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=["churn=1","churn=0"],normalise= False,
                      title="Confusion matrix")

print (classification_report(y_test, yhat))

#Logarithmic loss
#measures the performance of a classifier where the predicted output is a probability
#value between 0 and 1.

from sklearn.metrics import log_loss
log_loss(y_test, yhat_prob)
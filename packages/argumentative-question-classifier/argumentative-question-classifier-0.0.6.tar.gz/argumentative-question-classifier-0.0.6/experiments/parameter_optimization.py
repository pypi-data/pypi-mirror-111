from importlib.resources import path
import numpy as np
from sklearn import linear_model, datasets
from sklearn.model_selection import GridSearchCV
import pandas as pd
from conf.configuration import *
from argumentative_question_classifier.logistic_regression import LogisticRegressionClassifier
from sklearn.svm import LinearSVC
def prepare_feature_vectors():

    experiment_in_topic='experiment-questions-categories-in-topic'
    path_test=get_path_experiment_part(experiment_in_topic,0,'test')
    df_training=pd.read_csv(path_test,sep="\t",encoding="utf-8")
    lg = LogisticRegressionClassifier()
    lg.build_feature_space(df_training)
    features_vectors = lg.extract_feature_vectors(df_training)
    labels=df_training['annotation'].values
    return features_vectors,labels

def find_best_parameters(classifier,parameters,feature_vectors,labels):
    clf = GridSearchCV(classifier, parameters, cv=5, verbose=0)
    best_model=clf.fit(feature_vectors,labels)
    return best_model.best_estimator_.get_params()

def optimize_logisitc():
    feature_vectors,labels=prepare_feature_vectors()
    penalty = ['none', 'l2']
    C = np.ara
    max_iter=range(100,200)
    logistic = linear_model.LogisticRegression()
    hyperparameters = dict(C=C, penalty=penalty,max_iter=max_iter)
    best_model=find_best_parameters(logistic,hyperparameters,feature_vectors,labels)
    print(best_model)

def optimize_svm():
    feature_vectors,labels=prepare_feature_vectors()
    C= np.arange(0,10,0.01)
    svm  = LinearSVC()
    hyperparameters = dict(C=C)
    best_model=find_best_parameters(svm,hyperparameters,feature_vectors,labels)
    print(best_model)


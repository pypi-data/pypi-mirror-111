import nltk
import pandas as pd
from conf.configuration import *
from sklearn.metrics import cohen_kappa_score
def calculate_agreement():
    annotations_1 = read_annotations_1()
    annotations_2 = read_annotations_2()
    kappa_score = cohen_kappa_score(annotations_1,annotations_2)
    print("cohen_kappa is %f" %kappa_score)

def read_annotations_1():
    path = get_pilotstudy_dataset_annotator_path("yahoo","1")
    annotations = read_annotations(path)
    return annotations

def read_annotations_2():
    path = get_pilotstudy_dataset_annotator_path("yahoo","2")
    annotations = read_annotations(path)
    return annotations

def read_annotations(path):
    annotations_df = pd.read_csv(path,sep=",", encoding="utf-8")
    questions = list(annotations_df['question'])
    is_factoid=list(annotations_df['factoid'])
    is_method=list(annotations_df['method'])
    is_opinion=list(annotations_df['opinion'])
    is_argumentative=list(annotations_df['argumentative'])
    is_reason = list(annotations_df['reason'])
    annotations=[]
    for i,question in enumerate(questions):
        annotation =boolean_to_int(is_factoid[i],is_method[i],is_reason[i],is_argumentative[i],is_opinion[i])
        annotations.append(annotation)
    return annotations

def boolean_to_int(is_factoid,is_method,is_reason,is_argumentative,is_opinion):
    if is_factoid==1.0:
        return 0
    elif is_method==1.0:
        return 1
    elif is_reason==1.0:
        return 2
    elif is_argumentative==1.0:
        return  3
    elif is_opinion==1.0:
        return 4
    else:
        return 5


calculate_agreement()
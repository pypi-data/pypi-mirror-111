from sys import path

import pandas as pd
from conf.configuration import *
import logging
import numpy as np
logging.basicConfig(filename='pilot-stdyy-top-topics-analysis.log',level=logging.DEBUG)
worker_annotator_map={}
from annotation.kappa import fleiss_kappa
import matplotlib.pyplot as plt
from nltk.metrics.agreement import AnnotationTask
from nltk.metrics import interval_distance, binary_distance
from itertools import combinations
from collections import Counter

def get_index():
    index = ['factoid','method','argument','not-a-question','not-on-topic','others','opinion']
    return  index
def calc_annotator_per_question():
    path_toloka_result= get_path_part('pilot-study-top-topics-sample', 'results')
    df_results= pd.read_csv(path_toloka_result,sep="\t",encoding="utf-8")
    df_annotator_per_questions= df_results.groupby('INPUT:id').agg({'ASSIGNMENT:worker_id':pd.Series.nunique})
    print(df_annotator_per_questions.to_string())
def calc_inter_annotator_agreement(merge=None):
    path_toloka_result_with_annotator= get_path_part('pilot-study-top-topics-sample', 'results')
    if merge==None:
        df_results=pd.read_csv(path_toloka_result_with_annotator,sep="\t",encoding="utf-8",dtype={'OUTPUT:category':object,'ASSIGNMENT:worker_id':object,'INPUT:id':object}).sort_values('INPUT:id')
        df_results=df_results.drop(df_results[df_results['OUTPUT:category'].isnull()].index)
    else:
        df_results=merge_labels(merge)
    annotations=[]
    nltk_annotations=[]
    for index,row in df_results.iterrows():
        question_id = str(row['INPUT:id'])
        category = str(row['OUTPUT:category'])
        worker=str(row['ASSIGNMENT:worker_id'])
        nltk_annotations.append([worker,question_id,category])
        annotations.append((question_id,category))
    kappa= fleiss_kappa(annotations,3,7)
    t = AnnotationTask(nltk_annotations, distance=binary_distance)
    alpha = t.alpha()
    print("Fleiss's kappa is %f"%kappa)
    print("Krippendorf's alpha is %f"%alpha)

def calc_confusion_matrix():
    path_toloka_result_with_annotator= get_path_part('pilot-study-top-topics-sample', 'results')
    df_results=pd.read_csv(path_toloka_result_with_annotator,sep="\t",encoding="utf-8",dtype={'OUTPUT:category':object,'ASSIGNMENT:worker_id':object,'INPUT:id':object}).sort_values('INPUT:id')
    df_results=df_results.drop(df_results[df_results['OUTPUT:category'].isnull()].index)
    df_results = df_results.sort_values(['INPUT:id'])
    df_results['OUTPUT:category']=df_results['OUTPUT:category'].astype(int)
    df_count_annotators_per_question = df_results.groupby(by='INPUT:id', as_index=False).agg({'OUTPUT:category': pd.Series.nunique})
    df_cofused_question_ids=df_count_annotators_per_question[df_count_annotators_per_question['OUTPUT:category']>1]

    confusion_matrix=np.zeros(shape=(7,7))
    confused_annotations = pd.merge(right=df_cofused_question_ids[['INPUT:id']],left=df_results,on="INPUT:id",how='inner')
    path_results_confused=get_path_part('pilot-study-top-topics-sample', 'results_confused')
    confused_annotations.to_csv(path_results_confused,sep="\t",encoding='utf-8')


    aggregated_confused_annotations =confused_annotations.groupby('INPUT:id').agg({'OUTPUT:category':lambda confused_labels:list(combinations(confused_labels,2))})
    for index,row in aggregated_confused_annotations.iterrows():
        confused_pairs = row['OUTPUT:category']
        for confused_pair in confused_pairs:
            if confused_pair[0] != confused_pair[1]:
                confused_pair=sorted(confused_pair)
                confusion_matrix[confused_pair[0],confused_pair[1]]=confusion_matrix[confused_pair[0],confused_pair[1]]+1
    df_confusion_matrix=pd.DataFrame(confusion_matrix,index=get_index())
    index= get_index()
    index_map = {i:index[i] for i in range(0,7)}
    print(index_map)
    path_confusion_matrix = get_pilotstudy_dataset_analysis('pilot-study-top-topics-sample','toloka-confusion-matrix')
    print(path_confusion_matrix)
    visualize_confusion_matrix(confusion_matrix)
    df_confusion_matrix.rename(columns=index_map,inplace=True)
    df_confusion_matrix.to_csv(path_confusion_matrix,sep="\t",encoding='utf-8')

def visualize_confusion_matrix(confusion_matrix):
    labels=get_index()
    fig,ax = plt.subplots()
    ax.imshow(confusion_matrix,cmap="YlGn")
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    path_confusion_matrix_figure = get_pilotstudy_dataset_analysis('pilot-study-top-topics-sample','toloka-confusion-matrix-figure')
    fig.savefig(path_confusion_matrix_figure)


def calc_agreement_distribution():
    path_results_agreed= get_path_part('pilot-study-top-topics-sample', 'agreed')
    df_results_agreed= pd.read_csv(path_results_agreed,sep="\t",encoding="utf-8")
    distribution =df_results_agreed['annotation'].value_counts()
    print("labels distribution")
    print(distribution)

def calc_agreement_distribution_pave_sascha():
    path_results_agreed= get_pilotstudy_dataset_agreed_path('pilot-study-top-topics-sample')
    df_results_agreed= pd.read_csv(path_results_agreed,sep="\t",encoding="utf-8")
    distribution =df_results_agreed['annotation'].value_counts()
    print("labels distribution")
    print(distribution)

def calc_agreed():
    path_toloka_result_with_annotator= get_path_part('pilot-study-top-topics-sample', 'results')
    df_results=pd.read_csv(path_toloka_result_with_annotator,sep="\t",encoding="utf-8",dtype={'OUTPUT:category':object,'ASSIGNMENT:worker_id':object,'INPUT:id':object}).sort_values('INPUT:id')
    df_results=df_results.drop(df_results[df_results['OUTPUT:category'].isnull()].index)
    df_results = df_results.sort_values(['INPUT:id'])
    df_results['OUTPUT:category']=df_results['OUTPUT:category'].astype(int)
    df_count_annotators_per_question = df_results.groupby(by='INPUT:id', as_index=False).agg({'OUTPUT:category': pd.Series.nunique})
    df_results_without_agreement=df_count_annotators_per_question[df_count_annotators_per_question['OUTPUT:category']>=3]
    df_results_without_agreement=df_results_without_agreement[['INPUT:id']]
    df_results_with_agreement=df_count_annotators_per_question[df_count_annotators_per_question['OUTPUT:category']<3]
    df_results_majority_labels = df_results.groupby(by='INPUT:id', as_index=False).agg({'OUTPUT:category': lambda x:x.value_counts().index[0]})
    df_results_majority_labels.rename(columns={'OUTPUT:category':'annotation'},inplace=True)
    df_results_with_agreement = pd.merge(left=df_results_with_agreement[['INPUT:id']],right=df_results_majority_labels,on="INPUT:id",how='left')
    df_results_without_agreement['annotation']=[-1 for index in df_results_without_agreement.index]
    df_results_agreed= pd.concat([df_results_with_agreement,df_results_without_agreement])

    path_results_agreed= get_path_part('pilot-study-top-topics-sample', 'agreed')
    df_results_agreed.to_csv(path_results_agreed,sep="\t",encoding="utf-8",index=False)

def calc_agreement():
    path_toloka_result_with_annotator= get_path_part('pilot-study-top-topics-sample', 'results')
    df_results=pd.read_csv(path_toloka_result_with_annotator,sep="\t",encoding="utf-8").sort_values('INPUT:id')
    df_count_annotators_per_question = df_results.groupby(by='INPUT:id', as_index=False).agg({'OUTPUT:category': pd.Series.nunique}).set_index('INPUT:id')
    df_count_annotators_with_majority = df_results.groupby(by='INPUT:id', as_index=False).agg({'OUTPUT:category': lambda x:x.value_counts().index[0]})
    counts=df_count_annotators_with_majority['OUTPUT:category'].value_counts()
    print("agreed labels distribution")
    print(counts)
    print("agreement distribution")
    counts= df_count_annotators_per_question['OUTPUT:category'].value_counts()
    print(counts)

def merge(row,labels_to_be_merged):
    if row['OUTPUT:category'] in labels_to_be_merged:
        return 1000
    else:
        return row['OUTPUT:category']

def merge_labels(labels_to_merged):
    path_toloka_result_with_annotator= get_path_part('pilot-study-top-topics-sample', 'results')
    df_results=pd.read_csv(path_toloka_result_with_annotator,sep="\t",encoding="utf-8",dtype={'OUTPUT:category':object,'ASSIGNMENT:worker_id':object,'INPUT:id':object}).sort_values('INPUT:id')
    df_results=df_results.drop(df_results[df_results['OUTPUT:category'].isnull()].index)
    df_results['OUTPUT:category']=df_results.apply(lambda row:merge(row,labels_to_merged),axis=1)
    return  df_results


def calc_average_time():
    path_toloka_result_with_annotator= get_path_part('pilot-study-top-topics-sample', 'results')
    df_results=pd.read_csv(path_toloka_result_with_annotator,sep="\t",encoding="utf-8",parse_dates=True).sort_values('INPUT:id')

    df_results['ASSIGNMENT:started']=df_results.apply(lambda row:pd.to_datetime(row['ASSIGNMENT:started']),axis=1)
    df_results['ASSIGNMENT:submitted']=df_results.apply(lambda row:pd.to_datetime(row['ASSIGNMENT:submitted']),axis=1)

    df_results['time-spent']=df_results.apply(lambda row:(row['ASSIGNMENT:submitted'] - row['ASSIGNMENT:started']).total_seconds()/20.0,axis=1)
    df_results['time-spent']=df_results.apply(lambda row:(row['ASSIGNMENT:submitted'] - row['ASSIGNMENT:started']).total_seconds()/20.0,axis=1)
    print("average working time")
    print(df_results['time-spent'].mean())
    print("std working time")
    print(df_results['time-spent'].std())
    time_spent=list(df_results['time-spent'])
    bins = range(1,25)
    fig, ax = plt.subplots()
    ax.hist(time_spent,bins,histtype='bar', align='left',rwidth=0.5)
    ax.set(xlabel='seconds', ylabel='#annotations', title='Average working time')
    path_average_working_time=get_histogram_path_over('pilot-study-top-topics-sample','annotations','seconds')
    fig.savefig(path_average_working_time)

def correct_topics():
    path_corrected_questions=get_source_path('pilot-study-top-topics-sample-corrected')
    path_agreed_questions = get_pilotstudy_dataset_agreed_path('pilot-study-top-topics-sample')
    path_corrected_agreed_questions = get_pilotstudy_dataset_agreed_path('pilot-study-top-topics-sample-corrected')
    df_corrected_questions=pd.read_csv(path_corrected_questions,sep="\t",encoding="utf-8",index_col='question-id')
    df_agreed_questions = pd.read_csv(path_agreed_questions,sep="\t",encoding="utf-8",index_col='question-id')
    #print(df_corrected_questions.info())
    for index, question_row in df_agreed_questions.iterrows():
        corrected_topic= df_corrected_questions.loc[index,'topic']
        df_agreed_questions.loc[index,'topic']=corrected_topic
    df_agreed_questions=df_agreed_questions[df_agreed_questions['topic']!="Лебедев"]
    df_agreed_questions.to_csv(path_corrected_agreed_questions,sep="\t",encoding="utf-8")

#calc_confusion_matrix()
#calc_annotator_per_question()
#calc_inter_annotator_agreement()
#calc_agreement()
#calc_average_time()
#calc_agreed()
#calc_agreement_distribution()
#calc_agreement_distribution_pave_sascha()
correct_topics()
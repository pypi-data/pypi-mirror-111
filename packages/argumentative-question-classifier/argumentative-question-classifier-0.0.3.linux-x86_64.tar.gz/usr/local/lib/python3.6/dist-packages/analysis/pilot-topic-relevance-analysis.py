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
from sklearn.metrics import f1_score
from collections import Counter

def get_index():
    index = ['factoid','method','argument','not-a-question','not-on-topic','others','opinion']
    return  index


def read_annotations(batch):
    batch_label='batch-%d'%batch
    path_toloka_result= get_path_part('pilot-topic-relevance', batch_label + '-results')
    df_results= pd.read_csv(path_toloka_result,sep="\t",encoding="utf-8")
    df_results=df_results[df_results['INPUT:id']>0]
    return df_results

def read_annotations_filtered(batch):
    batch_label='batch-%d'%batch
    path_batch1_worker_accuracy= get_path_part('pilot-topic-relevance', batch_label + '-worker-accuracy')
    df_worker_accuracy=pd.read_csv(path_batch1_worker_accuracy,sep="\t",encoding="utf-8")
    df_good_workers=df_worker_accuracy[df_worker_accuracy['macro-f1']>=0.4]
    path_toloka_result= get_path_part('pilot-topic-relevance', batch_label + '-results')
    df_results= pd.read_csv(path_toloka_result,sep="\t",encoding="utf-8")
    df_results=df_results[df_results['INPUT:id']>0]
    df_results=df_results.merge(df_good_workers,on="ASSIGNMENT:worker_id")

    return df_results

def calc_annotator_per_question_filtered(batch):
    batch_label='batch-%d'%batch
    df_results=read_annotations_filtered(batch)
    df_annotator_per_questions= df_results.groupby('INPUT:id').agg({'ASSIGNMENT:worker_id':pd.Series.nunique})
    path_annotations_over_questions=get_histogram_path_over('pilot-topic-relevance',batch_label+'-annotation-filtered','question')
    df_annotator_per_questions.to_csv(path_annotations_over_questions,sep=",",encoding="utf-8")
    print(path_annotations_over_questions)

def calc_annotator_per_question(batch):
    batch_label='batch-%d'%batch
    df_results=read_annotations(batch)
    df_annotator_per_questions= df_results.groupby('INPUT:id').agg({'ASSIGNMENT:worker_id':pd.Series.nunique})
    path_annotations_over_questions=get_histogram_path_over('pilot-topic-relevance',batch_label+'-annotation','question')
    df_annotator_per_questions.to_csv(path_annotations_over_questions,sep=",",encoding="utf-8")
    print(path_annotations_over_questions)

def calc_inter_annotator_agreement(batch):

    df_results = read_annotations_filtered(batch)
    annotations=[]
    nltk_annotations=[]
    for index,row in df_results.iterrows():
        question_id = str(row['INPUT:id'])
        category = str(row['OUTPUT:category'])
        worker=str(row['ASSIGNMENT:worker_id'])
        nltk_annotations.append([worker,question_id,category])
        annotations.append((question_id,category))
    #kappa= fleiss_kappa(annotations,5,3)
    t = AnnotationTask(nltk_annotations, distance=binary_distance)
    alpha = t.alpha()
    #print("Fleiss's kappa is %f"%kappa)
    print("Krippendorf's alpha is %f"%alpha)

def calc_annotation_statistics(batch):
    batch_label='batch-%d'%batch
    path_batch1_quality_checks= get_path_part('pilot-topic-relevance', batch_label + '-quality-checks')
    df_batch1_quality_checks=pd.read_csv(path_batch1_quality_checks,sep="\t",encoding="utf-8")
    df_annotations=read_annotations(batch)
    df_annotations.rename(columns={'INPUT:id':'question-id'},inplace=True)
    df_quality_check_annotations=df_annotations.merge(df_batch1_quality_checks,on='question-id')

    print("Count of annotations of quality checks is %d"%df_quality_check_annotations.shape[0],)

    path_batch1_source= get_path_part('pilot-topic-relevance', batch_label + '-source')
    df_batch1_source=pd.read_csv(path_batch1_source,sep="\t",encoding="utf-8")
    print("count of questions to annotate is %d"%df_annotations.shape[0])
    print("count of source questions s %d"%df_batch1_source.shape[0])
    df_source_annotations=df_annotations.merge(df_batch1_source,on='question-id')
    df_source_annotations.to_csv('1.csv')




    print("Count of source annotations  %d"%df_source_annotations.shape[0])

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
    new_question_id=None
    categories=[]
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


def calc_agreement_distribution(batch):
    batch_label="batch-%d"%batch
    path_results_agreed= get_path_part('pilot-topic-relevance', batch_label + '-agreed')
    df_results_agreed=pd.read_csv(path_results_agreed,sep="\t",encoding="utf-8")
    distribution =df_results_agreed['annotation'].value_counts()
    print("labels distribution")
    print(distribution)


def calc_agreed(batch):
    batch_label="batch-%d"%batch
    df_results=read_annotations_filtered(batch)
    df_results=df_results.drop(df_results[df_results['OUTPUT:category'].isnull()].index)
    df_results = df_results.sort_values(['INPUT:id'])
    df_results['OUTPUT:category'] = df_results['OUTPUT:category'].astype(int)
    df_results_agreed = df_results.groupby(by='INPUT:id', as_index=False).agg({'OUTPUT:category': Counter})
    df_results_agreed['annotation'] = [-1 for index in df_results_agreed.index]
    df_results_agreed['is-quality-check'] = [0 for index in df_results_agreed.index]
    for index, row in df_results_agreed.iterrows():
        votes=row['OUTPUT:category'].values()
        sum_votes=float(sum(votes))
        max_votes=max(votes)
        label=row['OUTPUT:category'].most_common(1)[0][0]
        if max_votes/sum_votes>= 0.60:
            df_results_agreed.loc[index,'annotation']=label
        if max_votes/sum_votes>0.75 and sum_votes>2:
            df_results_agreed.loc[index,'is-quality-check']=1

    path_results_agreed= get_path_part('pilot-topic-relevance', batch_label + '-agreed')
    path_batch_source =get_path_part('pilot-topic-relevance', batch_label + '-source')
    path_batch_quality_checks =get_path_part('pilot-topic-relevance', batch_label + '-quality-checks')
    df_batch_source=pd.read_csv(path_batch_source,sep="\t",encoding="utf-8")
    df_batch_quality_checks=pd.read_csv(path_batch_quality_checks,sep="\t",encoding="utf-8")
    df_batch=pd.concat([df_batch_source])
    df_batch.rename(columns={'question-id':'INPUT:id'},inplace=True)

    df_results_agreed=df_results_agreed.merge(df_batch[['INPUT:id','topic','question']],on='INPUT:id')

    df_results_agreed['INPUT:id']=df_results_agreed['INPUT:id'].astype(int)
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


def calc_worker_accuracy(batch):
    batch_label="batch-%d"%batch
    path_batch1_quality_checks= get_path_part('pilot-topic-relevance', batch_label + '-quality-checks')
    df_batch1_quality_checks=pd.read_csv(path_batch1_quality_checks,sep="\t",encoding="utf-8")
    df_annotations=read_annotations(batch)
    df_annotations.rename(columns={'INPUT:id':'question-id'},inplace=True)
    df_quality_check_annotations=df_batch1_quality_checks.merge(df_annotations,on='question-id')
    worker_ids=[]
    f1_scores=[]
    for worker_id, df_quality_check_with_worker_id in list(df_quality_check_annotations.groupby('ASSIGNMENT:worker_id')):
        annotations=df_quality_check_with_worker_id['OUTPUT:category']
        gold_annotations=df_quality_check_with_worker_id['annotation']
        macro_f1=f1_score(gold_annotations,annotations,average="macro")
        f1_scores.append(macro_f1)
        worker_ids.append(worker_id)
    df_worker_accuracy=pd.DataFrame({'ASSIGNMENT:worker_id':worker_ids,'macro-f1':f1_scores})
    df_worker_accuracy.sort_values('macro-f1',inplace=True)
    df_annotations_per_annotator= df_annotations['ASSIGNMENT:worker_id'].value_counts().rename_axis('ASSIGNMENT:worker_id').to_frame('counts').reset_index()
    worker_accuracy_and_output=df_annotations_per_annotator.merge(df_worker_accuracy,on='ASSIGNMENT:worker_id')
    path_batch1_worker_accuracy= get_path_part('pilot-topic-relevance', batch_label + '-worker-accuracy')
    worker_accuracy_and_output.to_csv(path_batch1_worker_accuracy,sep="\t",encoding="utf-8")

#calc_inter_annotator_agreement()
#calc_annotator_per_question()
def reconstruct_source_batch(batch):
    path_non_training_non_ground_truth=get_source_path('pilot-topic-relevance')
    df_study=pd.read_csv(path_non_training_non_ground_truth,sep='\t',encoding="utf-8")
    batch_label="batch-%d"%batch
    path_batch_source =get_path_part('pilot-topic-relevance', batch_label + '-source')
    df_batch_source=pd.read_csv(path_batch_source,sep="\t",encoding="utf-8")
    df_batch_source=df_batch_source[['question-id']]
    df_batch_source=df_batch_source.merge(df_study,on='question-id')
    df_batch_source.to_csv(path_batch_source,sep="\t",encoding="utf-8",index=False)

for batch in range(1,5):
    #reconstruct_source_batch(batch)
    calc_worker_accuracy(batch)
    #calc_annotator_per_question_filtered(batch)
    #calc_annotator_per_question(batch)
    calc_inter_annotator_agreement(batch)
    calc_agreed(batch)
    calc_annotation_statistics(batch)
    calc_agreement_distribution(batch)
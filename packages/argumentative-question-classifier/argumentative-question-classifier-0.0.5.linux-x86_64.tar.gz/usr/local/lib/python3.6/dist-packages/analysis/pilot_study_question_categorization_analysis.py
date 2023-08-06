from nltk.metrics.agreement import AnnotationTask
from nltk.metrics import  binary_distance
from sklearn.metrics import f1_score
from collections import Counter
from conf.configuration import *
from mylogging import *
import logging
import pandas as pd
import numpy as np
from itertools import combinations
from annotation.kappa import fleiss_kappa
import simpledorff

logging.basicConfig(filename="../organization/pilot-study-question-categories-analysis.log",)
def get_index():
    index = ['factoid','method','argument','opinion','others']
    return  index

def read_annotations(study,batch):
    batch_label='batch-%d'%batch
    path_toloka_result= get_path_part(study, batch_label + '-results')
    df_results= pd.read_csv(path_toloka_result,sep="\t",encoding="utf-8")

    df_results.dropna(subset=['INPUT:id'],inplace=True)
    df_results['INPUT:id']=df_results['INPUT:id'].astype(int)
    df_only_questions=df_results[df_results['INPUT:id']>0]
    log(batch_label+"-results",df_results,"only-questions",df_only_questions, 'dropping topics')
    return df_only_questions

def read_annotations_filtered(study,batch,acceptance_threshold):
    batch_label='batch-%d'%batch

    path_batch1_worker_accuracy= get_path_part(study, batch_label + '-worker-accuracy')
    df_worker_accuracy=pd.read_csv(path_batch1_worker_accuracy,sep="\t",encoding="utf-8")
    df_good_workers=df_worker_accuracy[df_worker_accuracy['macro-f1']>=acceptance_threshold]
    df_workers_without_quality_measure=df_worker_accuracy[df_worker_accuracy['macro-f1'].isnull()]
    df_workers=pd.concat([df_good_workers, df_workers_without_quality_measure])
    logging.warning("count of rejected workers %d" %(df_worker_accuracy.shape[0]-df_good_workers.shape[0]))
    path_toloka_result= get_path_part(study, batch_label + '-results')
    df_results= pd.read_csv(path_toloka_result,sep="\t",encoding="utf-8")
    df_results.dropna(subset=['INPUT:id'],inplace=True)
    df_results['INPUT:id']=df_results['INPUT:id'].astype(int)
    df_results=df_results[df_results['INPUT:id']!=-1]
    df_results_filtered=df_results.merge(df_workers,on="ASSIGNMENT:worker_id")
    log('batch-%d-results-filtered'%batch,df_results_filtered,'batch-%d-results'%batch,df_results,'droping workers with quality less than %f'%acceptance_threshold)
    return df_results_filtered

def read_annotations_without_quality_checks(study,batch,acceptance_threshold):
    df_results=read_annotations_filtered(study,batch,acceptance_threshold)
    df_quality_checks=get_quality_checks_for(study,batch)

    df_results_wihtout_quality_checks=df_results[~df_results['INPUT:id'].isin(df_quality_checks['question-id'])]
    log_subtraction('results-without-quality-checks',df_results_wihtout_quality_checks,'results',df_results,"batch-%d-quality-checks"%batch,df_quality_checks)

    return df_results_wihtout_quality_checks

def get_quality_checks_for(study,batch):
    batch_label="batch-%d"%batch
    path_batch1_quality_checks= get_path_part(study, batch_label + '-quality-checks')
    df_batch1_with_quality_checks=pd.read_csv(path_batch1_quality_checks,sep="\t",encoding="utf-8")
    df_batch1_quality_checks=df_batch1_with_quality_checks[df_batch1_with_quality_checks['annotation'].isin([0,1,2,3,4])]
    log_message("batch-%d-quality-checks[%d]"%(batch,df_batch1_quality_checks.shape[0]))
    return df_batch1_quality_checks


def calc_worker_accuracy(study,batch):
    batch_label="batch-%d"%batch
    df_annotations=read_annotations(study,batch)
    df_annotations.rename(columns={'INPUT:id':'question-id'},inplace=True)
    df_batch1_quality_checks= get_quality_checks_for(study,batch)

    df_quality_check_annotations=df_batch1_quality_checks.merge(df_annotations,on='question-id')
    df_quality_check_annotations.to_csv('1.csv',sep="\t",encoding="utf-8")
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
    worker_accuracy_and_output=df_annotations_per_annotator.merge(df_worker_accuracy,on='ASSIGNMENT:worker_id',how='left')
    path_batch1_worker_accuracy= get_path_part(study, batch_label + '-worker-accuracy')
    worker_accuracy_and_output.to_csv(path_batch1_worker_accuracy,sep="\t",encoding="utf-8")

def calc_inter_annotator_agreement(study,batch,acceptance_threshold):
    df_results = read_annotations_filtered(study,batch,acceptance_threshold)

    annotations=[]
    nltk_annotations=[]
    for index,row in df_results.iterrows():
        question_id = str(row['INPUT:id'])
        category = str(row['OUTPUT:category'])
        worker=str(row['ASSIGNMENT:worker_id'])
        nltk_annotations.append([worker,question_id,category])
        annotations.append((question_id,category))
    kappa= fleiss_kappa(annotations,3,5)
    t = AnnotationTask(nltk_annotations, distance=binary_distance)
    alpha = t.alpha()
    print("Fleiss's kappa is %f"%kappa)
    logging.warning("NLTK Krippendorf's alpha is %f"%alpha)
    alpha= simpledorff.calculate_krippendorffs_alpha_for_df(df_results,experiment_col='INPUT:id',
                                                     annotator_col='ASSIGNMENT:worker_id',
                                                     class_col='OUTPUT:category')
    logging.warning("Simple dorff Krippendorf's alpha is %f"%alpha)
    return alpha

def calc_agreement_distribution(study,batch):
    batch_label="batch-%d"%batch
    path_results_agreed= get_path_part(study, batch_label + '-agreed')
    df_results_agreed=pd.read_csv(path_results_agreed,sep="\t",encoding="utf-8")
    logging.warning(f"agreed[{df_results_agreed.shape[0]}]")
    distribution =df_results_agreed['annotation'].value_counts()
    logging.warning("labels distribution")
    logging.warning(distribution)

    return dict(distribution)

def calc_confusion_matrix(study,batch):
    path_toloka_result_with_annotator= get_path_part(study, 'batch-%d-results'%batch)
    df_results=pd.read_csv(path_toloka_result_with_annotator,sep="\t",encoding="utf-8",dtype={'OUTPUT:category':object,'ASSIGNMENT:worker_id':object,'INPUT:id':object}).sort_values('INPUT:id')
    df_results=df_results.drop(df_results[df_results['OUTPUT:category'].isnull()].index)
    df_results = df_results.sort_values(['INPUT:id'])
    df_results['OUTPUT:category']=df_results['OUTPUT:category'].astype(int)
    df_count_annotators_per_question = df_results.groupby(by='INPUT:id', as_index=False).agg({'OUTPUT:category': pd.Series.nunique})
    df_cofused_question_ids=df_count_annotators_per_question[df_count_annotators_per_question['OUTPUT:category']>1]

    confusion_matrix=np.zeros(shape=(5,5))
    confused_annotations = pd.merge(right=df_cofused_question_ids[['INPUT:id']],left=df_results,on="INPUT:id",how='inner')




    aggregated_confused_annotations =confused_annotations.groupby('INPUT:id').agg({'OUTPUT:category':lambda confused_labels:list(combinations(confused_labels,2))})
    for index,row in aggregated_confused_annotations.iterrows():
        confused_pairs = row['OUTPUT:category']
        for confused_pair in confused_pairs:
            if confused_pair[0] != confused_pair[1]:
                confused_pair=sorted(confused_pair)
                confusion_matrix[confused_pair[0],confused_pair[1]]=confusion_matrix[confused_pair[0],confused_pair[1]]+1
    df_confusion_matrix=pd.DataFrame(confusion_matrix,index=get_index())
    index= get_index()
    index_map = {i:index[i] for i in range(0,5)}


    path_results_confused=get_path_part(study, 'batch-%d-results-confused'%batch)
    df_confusion_matrix.rename(columns=index_map,inplace=True)
    df_confusion_matrix.to_csv(path_results_confused,sep="\t",encoding='utf-8')


def calc_agreed(study,batch,acceptance_threshold):

    batch_label="batch-%d"%batch
    path_results_agreed= get_path_part(study, batch_label + '-agreed')


    path_batch_source =get_path_part(study, batch_label + '-source')
    df_results = read_annotations_filtered(study,batch,acceptance_threshold)
    #df_results = read_annotations_filtered(batch,study,acceptance_threshold)

    df_results=df_results.drop(df_results[df_results['OUTPUT:category'].isnull()].index)
    df_results = df_results.sort_values(['INPUT:id'])
    df_results['OUTPUT:category'] = df_results['OUTPUT:category'].astype(int)

    df_results_agreed = df_results.groupby(by='INPUT:id', as_index=False).agg({'OUTPUT:category': Counter})
    df_results_agreed['annotation'] = [-1 for index in df_results_agreed.index]
    df_results_agreed['is-quality-check'] = [0 for index in df_results_agreed.index]

    df_results_agreed['count.factoid']=df_results_agreed.apply(lambda row:row['OUTPUT:category'][0],axis=1)
    df_results_agreed['count.method']=df_results_agreed.apply(lambda row:row['OUTPUT:category'][1],axis=1)
    df_results_agreed['count.argumentative']=df_results_agreed.apply(lambda row:row['OUTPUT:category'][2],axis=1)
    df_results_agreed['count.opinion']=df_results_agreed.apply(lambda row:row['OUTPUT:category'][3],axis=1)
    df_results_agreed['count.others']=df_results_agreed.apply(lambda row:row['OUTPUT:category'][4],axis=1)
    df_results_agreed['count.annotations']=df_results_agreed.apply(lambda row:row['count.factoid']+row['count.method']+row['count.argumentative']+row['count.opinion']+row['count.others'],axis=1)

    for index, row in df_results_agreed.iterrows():
        votes=row['OUTPUT:category'].values()
        sum_votes=float(sum(votes))
        max_votes=max(votes)
        label=row['OUTPUT:category'].most_common(1)[0][0]
        if max_votes/sum_votes>= 0.60:
            df_results_agreed.loc[index,'annotation']=label
        if max_votes/sum_votes>0.75 and sum_votes>2:
            df_results_agreed.loc[index,'is-quality-check']=1

    df_batch_source=pd.read_csv(path_batch_source,sep="\t",encoding="utf-8")
    logging.warning("batch-%d-source[%d]"%(batch,df_batch_source.shape[0]))

    df_batch_source.rename(columns={'question-id':'INPUT:id'},inplace=True)

    df_results_agreed=df_results_agreed.merge(df_batch_source[['INPUT:id','topic','topic-id','question']],on='INPUT:id')

    df_results_agreed['INPUT:id']=df_results_agreed['INPUT:id'].astype(int)
    df_results_agreed.rename(columns={'INPUT:id':'question-id'},inplace=True)
    df_results_agreed.to_csv(path_results_agreed,sep="\t",encoding="utf-8",index=False)

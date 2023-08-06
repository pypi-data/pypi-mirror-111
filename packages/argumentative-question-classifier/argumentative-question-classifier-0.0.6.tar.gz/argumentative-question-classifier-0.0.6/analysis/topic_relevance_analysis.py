import pandas as pd
from conf.configuration import *
import logging


worker_annotator_map={}

from nltk.metrics.agreement import AnnotationTask
from nltk.metrics import  binary_distance
from sklearn.metrics import f1_score
from collections import Counter
from annotation.topic_relevance_task import *


batches_2nd_iter_final=[group_batch_map_2nd_iter[group][-1] for group in group_batch_map_2nd_iter]

def read_annotations(batch,study):
    batch_label='batch-%d'%batch
    path_toloka_result= get_path_part(study, batch_label + '-results')
    df_results= pd.read_csv(path_toloka_result,sep="\t",encoding="utf-8")
    df_results=df_results[df_results['INPUT:id']>0]
    return df_results

def read_annotations_without_quality_checks(batch,study):
    batch_label='batch-%d'%batch
    path_toloka_result= get_path_part(study, batch_label + '-results')
    df_results= pd.read_csv(path_toloka_result,sep="\t",encoding="utf-8")
    df_results=df_results[df_results['INPUT:id']>0]
    df_quality_checks=get_quality_checks_for(batch,study)
    df_results_wihtout_quality_checks=df_results[~df_results['INPUT:id'].isin(df_quality_checks['question-id'])]
    return df_results_wihtout_quality_checks

def read_annotations_filtered(batch,study):
    batch_label='batch-%d'%batch
    path_batch1_worker_accuracy= get_path_part(study, batch_label + '-worker-accuracy')
    df_worker_accuracy=pd.read_csv(path_batch1_worker_accuracy,sep="\t",encoding="utf-8")
    df_good_workers=df_worker_accuracy[df_worker_accuracy['macro-f1']>=0.4]
    logging.warning("count of rejected workers %d" %(df_worker_accuracy.shape[0]-df_good_workers.shape[0]))
    path_toloka_result= get_path_part(study, batch_label + '-results')
    df_results= pd.read_csv(path_toloka_result,sep="\t",encoding="utf-8")
    df_results=df_results[df_results['INPUT:id']>0]
    df_results=df_results.merge(df_good_workers,on="ASSIGNMENT:worker_id")

    return df_results

def read_annotations_filtered_2nd_iter(batch, study):

    if batch in batches_2nd_iter_final:
        df_annotations= read_annotations(batch,study)
        return df_annotations
    else:
        df_annotations_filtered = read_annotations_filtered(batch,study)
        group = get_group_for_batch(batch)
        batches_2nd_iter= group_batch_map_2nd_iter[group]
        df_annotations_2nd_iter_to_add_all=[]
        for batch in batches_2nd_iter:
            batch_label='batch-%d'%batch
            path_toloka_result= get_path_part('topic-relevance-2nd', batch_label + '-results')
            if os.path.exists(path_toloka_result):
                df_annotations_2nd_iter = read_annotations_without_quality_checks(batch,'topic-relevance-2nd')

                df_annotations_2nd_iter_to_add = df_annotations_2nd_iter[df_annotations_2nd_iter['INPUT:id'].isin(df_annotations_filtered['INPUT:id'])]
                df_annotations_2nd_iter_to_add_all.append(df_annotations_2nd_iter_to_add)
        df_annotations_2nd_iter_to_add_all.append(df_annotations_filtered)
        return pd.concat(df_annotations_2nd_iter_to_add_all)


def calc_annotator_per_question_filtered(batch,study):
    batch_label='batch-%d'%batch
    df_results=read_annotations_filtered(batch,study)

    df_annotator_per_questions= df_results.groupby('INPUT:id').agg({'ASSIGNMENT:worker_id':pd.Series.nunique})
    path_annotations_over_questions=get_histogram_path_over(study,batch_label+'-annotation-filtered','question')
    df_annotator_per_questions.to_csv(path_annotations_over_questions,sep=",",encoding="utf-8")

def calc_annotator_per_question(batch,study):
    batch_label='batch-%d'%batch
    df_results=read_annotations(batch,study)
    df_annotator_per_questions= df_results.groupby('INPUT:id').agg({'ASSIGNMENT:worker_id':pd.Series.nunique})
    path_annotations_over_questions=get_histogram_path_over(study,batch_label+'-annotation','question')
    df_annotator_per_questions.to_csv(path_annotations_over_questions,sep=",",encoding="utf-8")


def calc_inter_annotator_agreement(batch,study, iteration= None):

    if iteration ==2:
        df_results = read_annotations_filtered_2nd_iter(batch, study)
    else:
        df_results = read_annotations_filtered(batch,study)

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
    logging.warning("Krippendorf's alpha is %f"%alpha)

    return alpha

def calc_annotations_num(batch,study,df_annotations,with_quality_checks=True):

    if with_quality_checks:
        return df_annotations.shape[0]
    else:
        df_batch_quality_checks = get_quality_checks_for(batch,study)
        df_annotations.rename(columns={'INPUT:id':'question-id'},inplace=True)
        df_batch_quality_checks.rename(columns={'INPUT:id':'question-id'},inplace=True)
        df_quality_check_annotations = df_annotations.merge(df_batch_quality_checks,on='question-id')
        df_annotations_without_quality_checks = df_annotations[~df_annotations['question-id'].isin(df_quality_check_annotations['question-id'])]
        return df_annotations_without_quality_checks.shape[0]

def calc_annotation_statistics(batch,study):

    batch_label='batch-%d'%batch
    path_batch1_source= get_path_part(study, batch_label + '-source')
    df_batch1_source=pd.read_csv(path_batch1_source,sep="\t",encoding="utf-8")


    df_annotations=read_annotations(batch,study)
    if batch in batches_2nd_iter_final:
        df_filtered_annotations=df_annotations
    else:
        df_filtered_annotations=read_annotations_filtered(batch,study)
    df_filtered_annotations_2nd_iter= read_annotations_filtered_2nd_iter(batch,study)

    num_questions=df_batch1_source.shape[0]
    num_annt = calc_annotations_num(batch,study,df_annotations)
    num_annt_filtered_2nd_iter = calc_annotations_num(batch,study,df_filtered_annotations_2nd_iter)
    num_annt_filtered=calc_annotations_num(batch,study,df_filtered_annotations)

    num_annt_without_qc = calc_annotations_num (batch,study, df_annotations,False)
    num_annt_filtered_2nd_iter_wtihout_qc = calc_annotations_num(batch,study,df_filtered_annotations_2nd_iter,False)
    num_annt_filtered_without_qc = calc_annotations_num(batch,study,df_filtered_annotations,False)
    return num_questions, num_annt, num_annt_filtered, num_annt_filtered_2nd_iter, num_annt_without_qc, num_annt_filtered_without_qc,num_annt_filtered_2nd_iter_wtihout_qc


def calc_agreement_distribution(batch,study,iteration=None):
    batch_label="batch-%d"%batch
    if iteration==2:
        path_results_agreed= get_path_part(study, batch_label + '-agreed-2nd')
        print(batch)
        df_results_agreed=pd.read_csv(path_results_agreed,sep="\t",encoding="utf-8")
    else:
        path_results_agreed= get_path_part(study, batch_label + '-agreed')
        df_results_agreed=pd.read_csv(path_results_agreed,sep="\t",encoding="utf-8")
    distribution =df_results_agreed['annotation'].value_counts()
    logging.warning("labels distribution")
    logging.warning(distribution)

    return dict(distribution)


def calc_agreed(batch,study,iteration=None):

    batch_label="batch-%d"%batch
    if iteration == 2:
        path_results_agreed= get_path_part(study, batch_label + '-agreed-2nd')
    else:
        path_results_agreed= get_path_part(study, batch_label + '-agreed')


    path_batch_source =get_path_part(study, batch_label + '-source')

    if iteration == 2:
        df_results=read_annotations_filtered_2nd_iter(batch, study)
    else:
        df_results = read_annotations_filtered(batch,study)

    df_results=df_results.drop(df_results[df_results['OUTPUT:category'].isnull()].index)
    df_results = df_results.sort_values(['INPUT:id'])
    df_results['OUTPUT:category'] = df_results['OUTPUT:category'].astype(int)

    df_results_agreed = df_results.groupby(by='INPUT:id', as_index=False).agg({'OUTPUT:category': Counter})
    df_results_agreed['annotation'] = [-1 for index in df_results_agreed.index]
    df_results_agreed['is-quality-check'] = [0 for index in df_results_agreed.index]

    df_results_agreed['count.on-topic']=df_results_agreed.apply(lambda row:row['OUTPUT:category'][0],axis=1)
    df_results_agreed['count.not-on-topic']=df_results_agreed.apply(lambda row:row['OUTPUT:category'][1],axis=1)
    df_results_agreed['count.not-a-question']=df_results_agreed.apply(lambda row:row['OUTPUT:category'][2],axis=1)
    df_results_agreed['count.annotations']=df_results_agreed.apply(lambda row:row['count.on-topic']+row['count.not-on-topic']+row['count.not-a-question'],axis=1)

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

    df_results_agreed=df_results_agreed.merge(df_batch_source[['INPUT:id','topic','question']],on='INPUT:id')

    df_results_agreed['INPUT:id']=df_results_agreed['INPUT:id'].astype(int)

    df_results_agreed.to_csv(path_results_agreed,sep="\t",encoding="utf-8",index=False)

    #df_results_agreed_sample=df_results_agreed.sample(frac=0.1)
    #df_results_agreed_sample.to_csv(path_results_agreed_sample,sep="\t",encoding="utf-8",index=False)



def get_quality_checks_for(batch,study):
    batch_label="batch-%d"%batch
    path_batch1_quality_checks= get_path_part(study, batch_label + '-quality-checks')
    df_batch1_with_quality_checks=pd.read_csv(path_batch1_quality_checks,sep="\t",encoding="utf-8")
    df_batch1_quality_checks=df_batch1_with_quality_checks[df_batch1_with_quality_checks['annotation'].isin([0,1,2])]
    return df_batch1_quality_checks


def calc_worker_accuracy(batch,study):
    batch_label="batch-%d"%batch
    df_annotations=read_annotations(batch,study)
    df_annotations.rename(columns={'INPUT:id':'question-id'},inplace=True)
    df_batch1_quality_checks= get_quality_checks_for(batch,study)
    df_batch1_quality_checks.to_csv("1.csv",sep="\t",encoding="utf-8")
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
    path_batch1_worker_accuracy= get_path_part(study, batch_label + '-worker-accuracy')
    worker_accuracy_and_output.to_csv(path_batch1_worker_accuracy,sep="\t",encoding="utf-8")


def show_final_results_statistics():
    path_topic_relevance = get_path_part('topic-relevance','production')
    df_production=pd.read_csv(path_topic_relevance,sep="\t",encoding='utf-8')
    print(df_production['annotation'].value_counts().to_dict())
#batch=1
#calc_worker_accuracy(batch)
#calc_annotator_per_question_filtered(batch)
#calc_annotator_per_question(batch)
#calc_inter_annotator_agreement(batch)
#calc_agreed(batch)
#calc_annotation_statistics(batch)
#calc_agreement_distribution(batch)
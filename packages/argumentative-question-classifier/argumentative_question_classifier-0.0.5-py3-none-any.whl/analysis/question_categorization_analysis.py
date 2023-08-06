import logging
import pandas as pd
import numpy as np
from itertools import combinations
from annotation.kappa import fleiss_kappa
#import simpledorff
from nltk.metrics.agreement import AnnotationTask
from nltk.metrics import  binary_distance
from sklearn.metrics import f1_score
from collections import Counter, namedtuple
from conf.configuration import *
from mylogging import *
from utils.pandas_util import *
from annotation.pilot_question_categories import *
from collections import Counter,defaultdict,namedtuple
from annotation.question_categories import *

results_fields=['question-id', 'topic-id', 'annotation', 'high-factoid', 'high-argumentative', 'high-opinion', 'high-method', 'low-factoid', 'low-argumentative', \
        'low-opinion','low-method','high-all','all','is-quality-check','batch-0','batch-1','batch-2' ,\
    'batch-3','question','topic']
results_fields_without_index=[field for field in results_fields if field!='question-id']
annotation_fields = [field for field in results_fields if field not in ['topic', 'topic-id','question']]
num_iterations=4



def generate_results(study,group):
    log_message(f"generating group-{group}-results")
    path_group_results = get_path_part(study,'group-%d-results'%group)

    path_group= get_path_part(study,'group-%d'%group)
    df_group=pd.read_csv(path_group,sep="\t",encoding="utf")
    for field in results_fields:
        if field not in df_group.columns:
            df_group[field]=pd.NA
    df_group.to_csv(path_group_results, sep="\t", encoding="utf-8",  index=False)


def read_annotations(study,batch):
    batch_label='batch-%d'%batch
    path_toloka_result= get_path_part(study, batch_label + '-results')
    df_results= pd.read_csv(path_toloka_result,sep="\t",encoding="utf-8")

    df_results.dropna(subset=['INPUT:id'],inplace=True)
    df_results['INPUT:id']=df_results['INPUT:id'].astype(int)
    df_only_questions=df_results[df_results['INPUT:id']>0]
    df_batch_split=load_subdatset(study,'batch-%d-split'%batch,index_col=None)
    df_batch_split=df_batch_split[['question-id','topic-id','topic']]
    df_batch_split.rename(columns={'question-id':'INPUT:id'},inplace=True)
    df_only_questions=df_only_questions.merge(df_batch_split,on='INPUT:id')
    df_only_questions['OUTPUT:category']=df_only_questions['OUTPUT:category'].astype(int)
    log(batch_label+"-results",df_results,"only-questions",df_only_questions, 'dropping topics')
    return df_only_questions

def read_or_create_if_not_exists(path):
    if not os.path.exists(path):
        fields=['question-id','worker-id','annotation','topic-id','batch','gold-annotation','quality','topic']
        df_worker_results=pd.DataFrame(columns=fields)
        df_worker_results.to_csv(path,sep="\t",encoding="utf-8")
        return df_worker_results
    else:
        return pd.read_csv(path,sep="\t",encoding="utf-8")


def judge_batch_quality(df_batch_results,threshold):

    df_batch_results['quality']=''
    for worker_id, df_quality_check_with_worker_id in list(df_batch_results.groupby('worker-id')):
        df_quality_check_with_worker_id=df_quality_check_with_worker_id.dropna(subset=['gold-annotation'])
        annotations=df_quality_check_with_worker_id['annotation'].astype(int).values
        gold_annotations=df_quality_check_with_worker_id['gold-annotation'].astype(int).values
        worker_macro_f1=f1_score(gold_annotations,annotations,average="macro")

        if worker_macro_f1 >= threshold:
            worker_quality='high'
        else:
            worker_quality='low'

        for index,question_annotation in df_batch_results.iterrows():
            if question_annotation['worker-id']==worker_id:
                df_batch_results.loc[index,'quality']=worker_quality

    return df_batch_results


def drop_batch(df_worker_results, batch):
    df_worker_results=df_worker_results[df_worker_results['batch']!=batch]
    return df_worker_results

def drop_quality_checks(df_worker_results):
    return df_worker_results[df_worker_results['gold-annotation'].isna()]

def batch_exists(df_worker_results,batch):
    return batch in df_worker_results['batch'].unique()

#@profile
def add_batch_results(study,group,batch,threshold):
    df_batch=read_annotations(study,batch)
    label_worker_results='group-%d-worker-results'%group
    path_group_worker_results = get_path_part(study,label_worker_results)
    df_worker_results=read_or_create_if_not_exists(path_group_worker_results)
    df_batch=df_batch[['INPUT:id',"ASSIGNMENT:worker_id","OUTPUT:category","GOLDEN:category","INPUT:question","topic-id","topic"]]

    df_batch.rename(columns={'INPUT:id':'question-id','ASSIGNMENT:worker_id':'worker-id','OUTPUT:category':'annotation','GOLDEN:category':'gold-annotation'},inplace=True)
    df_batch['batch']=batch


    df_batch=judge_batch_quality(df_batch,threshold)
    if batch_exists(df_worker_results,batch):
        log_message(f"dropping existing {batch}  from  {label_worker_results}")
        log_size(label_worker_results,df_worker_results)
        df_worker_results=drop_batch(df_worker_results,batch)
    df_worker_results= pd.concat([df_worker_results, df_batch])
    log_size(label_worker_results,df_worker_results)
    df_worker_results.to_csv(path_group_worker_results,sep="\t",encoding="utf-8",index=False)


def get_batches(question_record,annotations):
    batches=sorted(annotations['batch'].unique())
    batches_formatted={f"batch-{batch_index}":batch for batch_index,batch in enumerate(batches)}
    for batch_index in range(num_iterations+1):
        batch_label = f"batch-{batch_index}"
        if batch_label not in batches_formatted:
            batches_formatted[batch_label]=pd.NA
    question_record.update(batches_formatted)

def map_to_scheme(scheme_reversed,annotation_counts,quality):
    readable_annotations= {quality+"-"+scheme_reversed[annotation]:count for annotation,count in sorted(annotation_counts.items())}
    for annotation in scheme_reversed.values():
        if (quality+"-"+annotation) not in readable_annotations:
            readable_annotations[quality+"-"+annotation]=0
    return readable_annotations
def count_annotations(question_record,annotations,quality):
    annotations=annotations['annotation'].values
    annotation_counts=Counter(annotations)
    readable_annotations= map_to_scheme(scheme_reversed,annotation_counts,quality)
    question_record.update(readable_annotations)


def get_annotation(question_record,high_annotations):
    if not isinstance(high_annotations,list):
        high_annotations=high_annotations['annotation'].values
    annotation_counts=Counter(high_annotations)
    votes=annotation_counts.values()
    sum_votes=float(sum(votes))
    label=-1
    if sum_votes>=3:
        max_votes=max(votes)
        if max_votes/sum_votes >=0.6: # 2 out of 3, 3 out of 5, 3 out of 4,
            label= annotation_counts.most_common(1)[0][0]
    question_record.update({"annotation":label})

def calc_batch_statistics(study,group,batch=None):
    df_batch_results = read_worker_group_results(study,group,batch)
    df_batch_results =drop_quality_checks(df_batch_results )
    num_questions= df_batch_results['question-id'].nunique()
    num_annotations =df_batch_results.shape[0]
    df_batch_results=df_batch_results[df_batch_results['quality']=='high']
    num_annotations_high=df_batch_results.shape[0]
    df_batch_question_quality = df_batch_results.groupby('question-id',as_index=False).agg({'quality':'count'}).rename(columns={"quality":"num_high"})
    num_questions_high=df_batch_question_quality[df_batch_question_quality ['num_high']==3].shape[0]
    BatchStatistics = namedtuple("BatchStatistics","questions questions_high annotations annotations_high")
    return BatchStatistics(num_questions,num_questions_high,num_annotations,num_annotations_high)

def get_quality_check(question_record,high_annotations):
    high_annotations=high_annotations['annotation'].values
    annotation_counts=Counter(high_annotations)
    votes=annotation_counts.values()
    sum_votes=float(sum(votes))

    is_quality_check=False
    if sum_votes>=3:
        max_votes=max(votes)
        if max_votes/sum_votes>=0.75:
            is_quality_check= True
    question_record.update({'is-quality-check':is_quality_check})

def update_group_results(study,group):
    path_group_worker_results = get_path_part(study,'group-%d-worker-results'%group)
    path_group_results = get_path_part(study,'group-%d-results'%group)

    dict_group_annotations_results={field:[] for field in annotation_fields}
    if os.path.exists(path_group_worker_results):
        df_worker_results=pd.read_csv(path_group_worker_results,sep="\t",encoding="utf-8",dtype={'annotation':int})
        df_worker_results=drop_quality_checks(df_worker_results)
        for question_id,question_annotations in list(df_worker_results.groupby('question-id')):
            question_record={'question-id':question_id}
            high_annotations=question_annotations[question_annotations['quality']=='high']
            low_annotations=question_annotations[question_annotations['quality']=='low']
            question_record.update({'all':len(question_annotations),'high-all':len(high_annotations)})
            count_annotations(question_record,high_annotations,'high')
            count_annotations(question_record,low_annotations,'low')
            get_batches(question_record,question_annotations)
            get_annotation(question_record,high_annotations)
            get_quality_check(question_record,high_annotations)
            for field in annotation_fields:
                dict_group_annotations_results[field].append(question_record[field])
        df_group_annotation_results=pd.DataFrame(dict_group_annotations_results)
        df_group_annotation_results.set_index('question-id',inplace=True)
        for column in df_group_annotation_results.columns:
                df_group_annotation_results[column]=df_group_annotation_results[column].astype(pd.Int64Dtype())

        df_group_results=pd.read_csv(path_group_results,sep="\t",encoding="utf-8",index_col='question-id')
        df_group_results.update(df_group_annotation_results)
        df_group_results.to_csv(path_group_results,sep="\t",encoding="utf-8",columns=results_fields_without_index)

def filter_group_results(df_group_results,batch=None,topic_id=None):

    if batch:
        for batch_iteration in range(0,num_iterations):
            df_group_results_filtered=df_group_results[df_group_results[f'batch-{batch_iteration}']==batch]
            if(df_group_results_filtered.shape[0]>0):
                break
    else:
        df_group_results_filtered=df_group_results
    if topic_id:
        df_group_results_filtered=df_group_results_filtered[df_group_results_filtered['topic_id']==topic_id]
    return df_group_results_filtered

def read_worker_group_results(study,group,batch=None,topic_id=None,quality=None):
    path_worker_results = get_path_part(study,"group-%d-worker-results"%group)
    df_worker_group_results= pd.read_csv(path_worker_results,sep="\t",encoding="utf-8",dtype={'annotation':int})
    df_worker_group_results=filter_worker_group_results(df_worker_group_results,batch,topic_id,quality)
    return df_worker_group_results

def filter_worker_group_results(df_worker_group_results,batch=None,topic_id=None,quality=None):
    if batch:
        df_worker_group_results = df_worker_group_results[df_worker_group_results['batch']==batch]
    if topic_id:
        df_worker_group_results = df_worker_group_results[df_worker_group_results['topic-id']==topic_id]
    if quality:
        df_worker_group_results = df_worker_group_results[df_worker_group_results['quality']==quality]
    return df_worker_group_results

def get_pretty_distribution(distribution):
    scheme_reversed_no_agreement = scheme_reversed.copy()
    scheme_reversed_no_agreement[-1]='no-agreement'
    return {scheme_reversed_no_agreement[annotation]:count for annotation,count in sorted(distribution.items())}

def calc_distribution(study,group, batch=None,topic_id=None):
    path_group_results = get_path_part(study,'group-%d-results'%group)
    df_group_results=pd.read_csv(path_group_results,sep="\t",encoding="utf-8",dtype={'annotation':pd.Int64Dtype()})
    df_group_results=filter_group_results(df_group_results,batch,topic_id)
    distribution = df_group_results['annotation'].value_counts().to_dict()
    for label in scheme.values():
        if label not in distribution:
            distribution[label]=0
    return distribution

def calc_confusion_matrix(study,group,batch=None,topic_id=None,quality=None):
    df_worker_group_results=read_worker_group_results(study,group,batch,topic_id,quality)
    df_worker_group_results=drop_quality_checks(df_worker_group_results)
    df_count_annotations = df_worker_group_results.groupby(by='question-id', as_index=False).agg({'annotation': pd.Series.nunique})
    df_cofused_question_ids=df_count_annotations[df_count_annotations['annotation']>1]

    confusion_matrix=np.zeros(shape=(4,4))
    df_confused_annotations = pd.merge(right=df_cofused_question_ids[['question-id']],left=df_worker_group_results,on="question-id",how='inner')
    df_aggregated_confused_annotations = df_confused_annotations.groupby('question-id').agg({'annotation':lambda confused_labels:list(combinations(confused_labels,2))})
    for index,row in df_aggregated_confused_annotations.iterrows():
        confused_pairs = row['annotation']
        for confused_pair in confused_pairs:
            if confused_pair[0] != confused_pair[1]:
                confused_pair=sorted(confused_pair)
                confusion_matrix[confused_pair[0],confused_pair[1]]=confusion_matrix[confused_pair[0],confused_pair[1]]+1
    return confusion_matrix

def calc_agreement_all(study,topic_id=None,quality=None):
    all_worker_group_results=[]
    for group in range(1,5):
        df_worker_group_results=read_worker_group_results(study,group,batch=None,topic_id=topic_id,quality=quality)
        all_worker_group_results.append(df_worker_group_results)
    df_all_worker_group_results=pd.concat(all_worker_group_results)
    nltk_annotations=[]
    for index,row in df_all_worker_group_results.iterrows():
        question_id = str(row['question-id'])
        category = str(row['annotation'])
        worker=str(row['worker-id'])
        nltk_annotations.append([worker,question_id,category])
    t = AnnotationTask(nltk_annotations, distance=binary_distance)
    return t.alpha()
def calc_agreement(study,group,batch=None,topic_id=None,quality=None):
    df_worker_group_results=read_worker_group_results(study,group,batch,topic_id,quality)
    nltk_annotations=[]
    for index,row in df_worker_group_results.iterrows():
        question_id = str(row['question-id'])
        category = str(row['annotation'])
        worker=str(row['worker-id'])
        nltk_annotations.append([worker,question_id,category])
    t = AnnotationTask(nltk_annotations, distance=binary_distance)
    return t.alpha()

def run_question_categories_batch_analysis(study):
    path_log_analysis=get_path_log_analysis(study)
    setup_logging(path_log_analysis)
    path_batches=get_path_batches(study)
    df_batches=pd.read_csv(path_batches,sep=",",encoding="utf-8",dtype={'run':bool})

    df_batches=df_batches[df_batches['run']==True]


    batches=[]
    batches_by_group=defaultdict(list)
    for index,batch_record in df_batches.iterrows():
        batch, group = batch_record['batch'],batch_record['group']
        log_message(f"{batch} is added")
        add_batch_results(study,group,batch,batch_record['quality-threshold'])

        batches.append(batch)
        batches_by_group[group].append(batch)
    batch_analysis=defaultdict(list)

    for group in batches_by_group:
        #generate_results(study,group)
        update_group_results(study,group)
        for batch in batches_by_group[group]:
            batch_record={}
            distribution = calc_distribution(study,group,batch)
            pretty_distribution= get_pretty_distribution(distribution)
            log_message(f"batch-{batch} analyzed")
            batch_record.update(pretty_distribution)
            confusion_matrix = calc_confusion_matrix(study,group,batch)

            log_matrix(confusion_matrix,scheme.keys(),scheme.keys())
            agreement = calc_agreement(study,group=group,batch=batch,topic_id=None,quality='high')
            batch_record.update({'batch':batch,'agreement':agreement})
            log_message(f"batch-{batch} has agreement {agreement}\n")
            batch_statistics=calc_batch_statistics(study,group,batch)
            batch_record.update({'questions':batch_statistics.questions,'questions-high':batch_statistics.questions_high,'annotations':batch_statistics.annotations,'annotations-high':batch_statistics.annotations_high})
            for column in batch_record:
                batch_analysis[column].append(batch_record[column])



    for column in batch_analysis:
        print(column)
        print(len(batch_analysis[column]))
    df_batch_analysis=pd.DataFrame(batch_analysis)
    all_row=df_batch_analysis.sum(axis=0)
    all_row.loc['agreement']=calc_agreement_all(study)
    all_row.loc['batch']="all"
    path_batch_analysis=get_path_analysis(study,'batches')
    df_batch_analysis=df_batch_analysis.append(all_row,ignore_index=True)
    df_batch_analysis.to_csv(path_batch_analysis,sep="\t",encoding="utf-8",columns=['batch','agreement','questions','questions-high','factoid','method','argumentative','opinion','no-agreement',
                                                                                    'annotations','annotations-high'
                                                                                    ],index=False)
def produce_production_dataset(study):
    all_gorups=[]
    for group in [1,2,3,4]:
        path_group_final=get_path_part(study,'group-%d-production'%group)
        path_group_results = get_path_part(study,'group-%d-results'%group)
        df_group_results = pd.read_csv(path_group_results,sep="\t",encoding="utf-8")
        df_group_production = df_group_results[['question-id','topic-id','question','annotation','topic']]
        df_group_production.to_csv(path_group_final,sep="\t",encoding="utf-8",index=False)
        all_gorups.append(df_group_production)
    df_production=pd.concat(all_gorups)
    path_production=get_path_part(study,'production')
    print(df_production['annotation'].value_counts())
    #todo
    df_production=df_production[~df_production['annotation'].isna()]

    df_production['annotation']=df_production['annotation'].astype(int)
    df_production.to_csv(path_production,sep="\t",encoding="utf-8",index=False)

def flatten_annotations(question_record):
    annotations=[]
    for label in scheme.keys():
        pretty_label=f"high-{label}"
        annotation=scheme[label]
        votes=question_record[pretty_label]
        flattened_votes= [annotation] * votes
        annotations.extend(flattened_votes)
    return annotations


def merge_annotations(high_annotations, merge_map):
    for i,annotation in enumerate(high_annotations):
        if annotation in merge_map:
            high_annotations[i]=merge_map[annotation]



def produce_production_dataset_merge(study,merge_map):
    all_gorups=[]
    for group in [1,2,3,4]:
        path_group_final=get_path_part(study,'group-%d-production-labels'%group)
        path_group_results = get_path_part(study,'group-%d-results'%group)
        df_group_results = pd.read_csv(path_group_results,sep="\t",encoding="utf-8")
        df_group_results['merged-annotation']=-1
        for index, question_record in df_group_results.iterrows():
            high_annotations=flatten_annotations(question_record)
            merge_annotations(high_annotations,merge_map)
            annotation_merged={}
            get_annotation(annotation_merged,high_annotations)
            df_group_results.loc[index,'merged-annotation']=annotation_merged['annotation']
        df_group_production = df_group_results[['question-id','topic-id','question','merged-annotation','topic']]
        df_group_production.rename(columns={'merged-annotation':'annotation'},inplace=True)
        df_group_production.to_csv(path_group_final,sep="\t",encoding="utf-8",index=False)
        all_gorups.append(df_group_production)
    df_production=pd.concat(all_gorups)
    path_production=get_path_part(study,'production-labels-merged')
    df_production=df_production[~df_production['annotation'].isna()]
    df_production['annotation']=df_production['annotation'].astype(int)
    df_production.to_csv(path_production,sep="\t",encoding="utf-8",index=False)

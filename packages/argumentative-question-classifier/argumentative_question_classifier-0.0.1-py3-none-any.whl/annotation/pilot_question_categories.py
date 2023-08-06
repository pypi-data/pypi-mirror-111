
from conf.configuration import *
import logging
from datetime import datetime
import pandas as pd
from mylogging import *
import numpy as np
import os.path
import random
import numpy
from scipy.stats import skew
import math

import copy
def get_path(study,part,step=None):
    if 'preprocessed' in part:
        path_dataset=get_preprocessed_path(study,step)
    else:
        path_dataset= get_path_part(study,part)
    return path_dataset

def load_subdatset(study,part,step=None,index_col="question-id",log=False):
    path_dataset=get_path(study,part,step)
    if log:
        log_path(path_dataset,part,False)

    if index_col==None:
        df=pd.read_csv(path_dataset,sep="\t",encoding="utf-8")
    else:
        df=pd.read_csv(path_dataset,sep="\t",encoding="utf-8",index_col=index_col)
    return df

def shuffle_dataframe(df,column=None):
    if column==None:
        return df.sample(frac=1)
    else:
        groups = [ sub_df.sample(frac=1) for _,sub_df in df.groupby(column) ]
        sampled_df = pd.concat(groups)
        return sampled_df

def save_subdataset(study,part,subdataset,step=None,save_index=True,log=False,check_existence=True):

    path_dataset=get_path(study,part,step)
    if check_existence:
        if not os.path.exists(path_dataset):
            subdataset.to_csv(path_dataset,sep="\t",encoding="utf-8",index=save_index)
        else:
            return
    else:
        subdataset.to_csv(path_dataset,sep="\t",encoding="utf-8",index=save_index)
    if log:
        log_path(path_dataset,part)

def initialize_logging(study):

    path_log=get_path_log(study)
    logging.basicConfig(filename=path_log,format='%(message)s')
    logging.warning(datetime.now())

def add_topic(df_question):

    path_top_topics_translated=get_path_described_topics('top-topics')
    df_top_topics_translated=pd.read_csv(path_top_topics_translated,sep='\t',encoding="utf-8",dtype={'topic':str})
    df_topics=df_top_topics_translated[['topic','topic-id']]
    df_question.reset_index(inplace=True)

    df_question=df_question.merge(df_topics,on='topic',how='left')
    df_question.set_index('question-id',inplace=True)
    return df_question

def drop_lebedev(study,is_production):

    path_source=get_source_path(study)
    df_question=pd.read_csv(path_source,sep="\t",encoding="utf-8",index_col='question-id')
    del df_question['phrase-id']
    df_question_without_lebedev = df_question[df_question['topic-id']!=16]
    df_question_without_deathpenalty = df_question_without_lebedev[df_question_without_lebedev['topic-id']!=3]
    log('preprocessed-1',df_question_without_deathpenalty,'source',df_question,"lebedev[61]+deathpenalty")
    save_subdataset(study,'preprocessed',df_question_without_deathpenalty,step=1,check_existence=is_production)

def drop_not_on_topic(study,is_production):
    df_ground_truth_not_topic=load_subdatset(study,'ground-truth-not-on-topic')
    df_questions=load_subdatset(study,'preprocessed',1)
    df_ground_truth_training=df_ground_truth_not_topic[~df_ground_truth_not_topic['annotation'].isin([3,4])]
    df_ground_truth_training=df_ground_truth_training[['question','topic','annotation']]
    df_ground_truth_training=add_topic(df_ground_truth_training)
    df_questions_on_topic=df_questions.loc[df_questions.index.isin(df_ground_truth_training.index)]

    save_subdataset(study,'preprocessed',df_questions_on_topic,step=2,check_existence=is_production)
    log('preprocessed-2',df_questions_on_topic,'preprocessed-1',df_questions,'[not-on-topic + not-a-question]')

    df_ground_truth_training=df_ground_truth_training[df_ground_truth_training['annotation']!=-1]
    df_ground_truth_training=change_scheme(df_ground_truth_training)

    save_subdataset(study,'ground-truth-training',df_ground_truth_training,check_existence=is_production)

    log('ground-truth-training',df_ground_truth_training,'ground-truth-not-on-topic',df_ground_truth_not_topic,'[not-on-topic + not-a-question + no-agreement]')

def filter_on_topic_questions(study,is_production):
    drop_lebedev(study,is_production)
    drop_not_on_topic(study,is_production)

def change_scheme(dataset):
    def change_annotation(annotation):
        if annotation == 6: #opinion
            return 3
        elif annotation == 5: #others
            return 4
        else:
            return annotation
    dataset['mapped-annotation']=dataset.apply(lambda row: change_annotation(row['annotation']),axis=1)
    del dataset['annotation']
    dataset.rename(columns={'mapped-annotation':'annotation'},inplace=True)
    return dataset

def filter_examples(study):

    df_ground_truth_examples = load_subdatset(study,'ground-truth-examples')
    questions_with_topics=df_ground_truth_examples.groupby('topic')
    examples=[]

    indices=[random.randint(100000,100100) for i in range(1,75)]
    index_counter=0
    for topic, topic_questions in questions_with_topics:
        topic_id=topic_questions.iloc[0,topic_questions.columns.get_loc('topic-id')]
        for annotation in range(0,5):
            df_annotaiton_example=topic_questions[topic_questions['annotation']==annotation]
            if df_annotaiton_example.shape[0]!=0:
                examples.append(df_annotaiton_example.sample(n=1).reset_index())
            else:
                next_index=indices[index_counter]
                examples.append(pd.DataFrame({'topic':[topic],'topic-id':topic_id,'question-id':[next_index],'question':["To-Add"],'annotation':annotation}))
                index_counter=index_counter + 1

    df_examples=pd.concat(examples)
    df_examples.set_index('question-id',inplace=True)
    df_ground_truth_no_examples=df_ground_truth_examples [~df_ground_truth_examples.index.isin(df_examples.index)]
    log_sample('examples',df_examples,'ground-truth-examples',df_ground_truth_examples,float(5*19/df_ground_truth_examples.shape[0]))

    return df_examples,df_ground_truth_no_examples


def filter_training(study,trianing_size):
    df_ground_truth_training=load_subdatset(study,'ground-truth-training')
    df_death_penalty=df_ground_truth_training[df_ground_truth_training['topic-id']==3]
    save_subdataset(study,'training-source',df_death_penalty)
    log('training-source',df_death_penalty,'ground-truth',df_ground_truth_training,'death penalty')


    df_training=df_death_penalty.sample(n=trianing_size)
    while df_training['annotation'].unique().shape[0]<4:
        df_training=df_death_penalty.sample(n=trianing_size)

    df_ground_truth= df_ground_truth_training[~df_ground_truth_training.index.isin(df_death_penalty.index)]
    log_sample('training',df_training,'training-source',df_death_penalty,float(trianing_size/df_death_penalty.shape[0]))
    return df_training,df_ground_truth

def filter_training_and_examples(study,is_production,training_size):
    df_ground_truth_training= load_subdatset(study,'ground-truth-training')

    df_training,df_ground_truth_examples=filter_training(study,training_size)
    save_subdataset(study,"training",df_training,check_existence=is_production)
    save_subdataset(study,'ground-truth-examples',df_ground_truth_examples,check_existence=is_production)
    log_subtraction('ground-truth-examples',df_ground_truth_examples,'ground-truth-training',df_ground_truth_training,"training-source",load_subdatset(study,'training-source'))

    df_examples,df_ground_truth=filter_examples(study)
    save_subdataset(study,'examples',df_examples,check_existence=is_production)
    save_subdataset(study,'ground-truth',df_ground_truth,check_existence=is_production)
    log_subtraction("ground-truth",df_ground_truth,'ground-truth-examples',df_ground_truth_examples,'examples',df_examples)

def sample_quality_checks(study,percentage):

    df_ground_truth=load_subdatset(study,'ground-truth')
    df_quality_checks=df_ground_truth.sample(frac=percentage)
    log_sample('quality-checks',df_quality_checks,'ground-truth',df_ground_truth,percentage)

    return df_quality_checks

def generate_study_and_quality_checks(study,is_production):

    df_question=load_subdatset(study,'preprocessed',step=2)
    df_quality_checks=sample_quality_checks(study,0.4)
    df_study=df_question[~df_question.index.isin(df_quality_checks.index)]
    save_subdataset(study,'quality-checks',df_quality_checks,check_existence=is_production)
    save_subdataset(study,'study-examples',df_study,check_existence=is_production)
    log_subtraction('study-examples',df_study,'preprocessed-2',df_question,'quality-checks',df_quality_checks)

def fitler_example_from_study(study,is_production):
    df_study_with_examples=load_subdatset(study,'study-examples')
    df_examples=load_subdatset(study,'examples')
    df_study=df_study_with_examples[~df_study_with_examples.index.isin(df_examples.index)]
    save_subdataset(study,'study',df_study,check_existence=is_production)
    log_subtraction('study',df_study,'study-examples',df_study_with_examples,'examples',df_examples)

def split_into_batches(study,num_batches,is_production):
    df_study=load_subdatset(study,'study')
    df_study=shuffle_dataframe(df_study)

    batches= np.array_split(df_study,num_batches)
    labels=["batch-%d"%batch for batch in range(1,num_batches+1)]
    for i,label in enumerate(labels):

        save_subdataset(study,label+"-source",batches[i],check_existence=is_production)
    source_labels=[label+"-source" for label in labels]
    log_split('study',df_study,source_labels,batches)
    return labels,batches

def split_batch_into_task_pages(study,batch,task_page_size,is_production):
    task_page_id=1
    def split_topic_questions(df_questions_topic_group):
        nonlocal task_page_id
        nonlocal task_page_size

        if questions_topic_group.shape[0] < task_page_size:
            questions_topic_group['task-page-id']=task_page_id
            task_page_id = task_page_id + 1
            return [questions_topic_group]
        else:
            task_pages_num=math.ceil(df_questions_topic_group.shape[0]/task_page_size)
            batch_splits=np.array_split(df_questions_topic_group.sort_values('order'),task_pages_num)
            for split in batch_splits:
                split['task-page-id']=task_page_id
                task_page_id=task_page_id+1
            return batch_splits

    df_batch=load_subdatset(study,batch+'-quality-checks')
    questions_topic_group=df_batch.groupby('topic-id')
    questions_topic_splits=[]

    for topic_id, questions_topic_group in questions_topic_group:
        questions_topic_group_split=split_topic_questions(questions_topic_group)
        questions_topic_splits.extend(questions_topic_group_split)

    log_message("Number of task pages is %d"%len(questions_topic_splits))
    df_batch_split=pd.concat(questions_topic_splits)

    save_subdataset(study,batch+'-split',df_batch_split,check_existence=is_production)


def get_quality_checks_source(batch):
    batch_number=batch[-1:]
    batch_number=int(batch_number)
    if batch_number==1:
        return "quality-checks"
    else:
        quality_checks_batch_number=batch_number-1
    return "batch-%d-agreed"%quality_checks_batch_number

def subdataset_exists(study,part,step=None):

    path=get_path(study,part,step)
    return os.path.exists(path)


def distribute_quality_checks(df_batch, task_page_size):

    topic_groups=df_batch.groupby('topic-id')
    df_batch['order']=range(1,df_batch.shape[0]+1)
    order=0
    for _,topic_group in topic_groups:
        order = order +1
        df_quality_checks=topic_group[topic_group['annotation'].isin([0,1,2,3,4])]
        counter=0
        topic_orders=[order]
        # assign orders to all questions
        for index,_ in topic_group.iterrows():
            df_batch.loc[index,'order']=order
            counter =counter +1
            if counter % task_page_size == 0:
                order= order+1
                topic_orders.append(order)


        # assign orders to qualit checks
        topic_orders_set=(copy.deepcopy(topic_orders))
        for index,_ in df_quality_checks.iterrows():
            if len(topic_orders_set)==0:
                topic_orders_set=(copy.deepcopy(topic_orders))
            elif len(topic_orders_set) ==1:
                topic_order_index=0
            else:
                topic_order_index=np.random.randint(0,len(topic_orders_set)-1)
            topic_order=topic_orders_set[topic_order_index]
            df_batch.loc[index,'order']=topic_order
            topic_orders_set.remove(topic_order)
    df_batch=df_batch.sort_values('order')
    df_batch=shuffle_dataframe(df_batch,'order')
    save_subdataset('temp','1',df_batch,check_existence=False)
    return df_batch

def add_quality_check(study,batch,quality_checks_ratio,task_page_size,is_production):

    df_batch_source=load_subdatset(study,batch+'-source')
    batch_size =df_batch_source.shape[0]
    quality_checks_size=int(batch_size*quality_checks_ratio)
    per_annotation_size=int(quality_checks_size/5)
    quality_check_source=get_quality_checks_source(batch)
    if subdataset_exists(study,quality_check_source):
        df_quality_checks_source=load_subdatset(study,quality_check_source)
        print(batch)
        df_quality_checks_source=df_quality_checks_source[df_quality_checks_source['annotation'].isin([0,1,2,3,4])]
        df_quality_checks_source=df_quality_checks_source[['topic-id','question','topic','annotation']]
        quality_checks_groups=df_quality_checks_source.groupby('annotation')
        sampled_quality_checks=[]
        for annotation,quality_checks_group in quality_checks_groups:
            quality_checks_group['annotation']=annotation
            if per_annotation_size > quality_checks_group.shape[0]:
                sampled_quality_checks.append(quality_checks_group)
            else:
                quality_checks_sample=quality_checks_group.sample(per_annotation_size)
                sampled_quality_checks.append(quality_checks_sample)
        batch_quality_checks=batch+"-quality-checks"
        df_batch_quality_checks=pd.concat(sampled_quality_checks)
        save_subdataset(study,batch+'-quality-checks-to-add',df_batch_quality_checks,log=True,check_existence=is_production)
        df_batch_quality_checks=load_subdatset(study,batch+'-quality-checks-to-add')
        log_sample(batch_quality_checks+'-to-add',df_batch_quality_checks,quality_check_source,df_quality_checks_source,quality_checks_ratio)
        df_batch_with_quality_checks=pd.concat([df_batch_quality_checks, df_batch_source])
        distribute_quality_checks(df_batch_with_quality_checks,task_page_size)
        log_addition(batch_quality_checks,df_batch_with_quality_checks,batch+"-split",df_batch_source,batch_quality_checks+'-to-add',df_batch_quality_checks)
        save_subdataset(study,batch_quality_checks,df_batch_with_quality_checks,check_existence=is_production)
        return True
    else:
        log_message("%s is still in progress"%quality_check_source)
        return False

def add_examples(study,batch,is_production):


    def rename_columns(df_examples):

        df_examples.rename(columns={0:'example-fact',1:'example-method',2:'example-argument',3:'example-opinion',4:'example-others'},inplace=True)
        df_examples['question']='question'
        df_examples['question-id']=-1
        df_examples['topic']=topic
        df_examples['topic-id']=topic_id
        df_examples['task-page-id']=task_page_id
        df_examples.set_index('question-id',inplace=True)

    def add_example_columns(df_batch):
        for label in ['fact','method','argument','opinion','others']:
            df_batch['example-'+label]='example-'+label

    df_batch_split = load_subdatset(study,batch+'-split')

    if batch=="training":
        df_examples = load_subdatset(study,'training-examples-to-add')
    else:
        df_examples = load_subdatset(study,'examples')


    add_example_columns(df_batch_split)
    task_pages_groups=df_batch_split.groupby('task-page-id')
    batch_examples=[]
    for task_page_id,task_page_group in task_pages_groups:

        topic_id=task_page_group.iloc[0,task_page_group.columns.get_loc('topic-id')]
        topic=task_page_group.iloc[0,task_page_group.columns.get_loc('topic')]
        df_topic_examples=df_examples [df_examples ['topic-id']==topic_id]
        df_topic_examples = df_topic_examples[['topic-id','annotation','question']]
        df_topic_examples=df_topic_examples.pivot(index='topic-id',columns='annotation',values='question')
        rename_columns(df_topic_examples)

        batch_examples.append(df_topic_examples)

    df_batch_examples=pd.concat(batch_examples)
    df_batch_with_examples=pd.concat([df_batch_examples, df_batch_split])

    save_subdataset(study,batch+'-examples',df_batch_with_examples,check_existence=is_production)
    log_addition('batch-examples',df_batch_with_examples,batch+'-split',df_batch_split,'examples',df_batch_examples)



def save_batch_with_toloka_columns(df_batch,path_batch):
    df_batch = df_batch[['question','question-id','task-id','annotation','example-fact',\
                'example-method','example-opinion','example-argument','example-others']].rename(
        columns={'question-id':"INPUT:id",'task-id':"INPUT:task-id","question":"INPUT:question","annotation":"GOLDEN:category"
            ,"example-fact":"INPUT:example-fact","example-method":"INPUT:example-method","example-opinion":"INPUT:example-opinion",
              'example-argument':"INPUT:example-argument", "example-others":"INPUT:example-others"
                 })
    df_batch['GOLDEN:category']=df_batch['GOLDEN:category'].fillna(-1).astype(int)
    df_batch['GOLDEN:category'].loc[df_batch['GOLDEN:category']==-1]=""

    df_batch.to_csv(path_or_buf=path_batch,sep="\t",encoding="utf-8",columns=['INPUT:id','INPUT:question','INPUT:example-fact','INPUT:example-method','INPUT:example-argument','INPUT:example-opinion','INPUT:example-others',"INPUT:task-id",'GOLDEN:category'],index=False)

def save_formmated_tasks(path_batch_final,path_batch_formatted,last_question_id_per_task_page):
    skip_header=False
    count_of_lines=0
    with open(path_batch_final,'r') as file_annotation_tasks:
        with open(path_batch_formatted,'w') as file_annotation_tasks_batches:
            for line in file_annotation_tasks:
                if not skip_header:
                    file_annotation_tasks_batches.write(line)
                    skip_header=True
                    count_of_lines=count_of_lines+1
                    continue
                question_id = line.split('\t')[0]
                if int(question_id) in list(last_question_id_per_task_page):
                    file_annotation_tasks_batches.write(line+"\n")
                    count_of_lines=count_of_lines+1
                else:
                    file_annotation_tasks_batches.write(line)
                count_of_lines=count_of_lines+1
    logging.warning("batch-fromatted[%d] <- batch[%d]"%(count_of_lines,pd.read_csv(path_batch_final,sep="\t",encoding="utf-8").shape[0]))


def format(study,batch):


    df_batch=load_subdatset(study,batch+'-examples',index_col=None)
    # shuffle
    #df_batch=shuffle_dataframe(df_batch,'task-page-id')
    # sort
    df_batch['temp-id']=df_batch.apply(lambda row:row['question-id']>0,axis=1)
    df_batch.sort_values(['topic-id','task-page-id','temp-id'],inplace=True)
    df_batch['task-id']=-1
    task_page_groups=df_batch.groupby('task-page-id')
    for _, task_page in task_page_groups:
        df_batch.loc[task_page.index,'task-id']=range(0,len(task_page))

    last_question_id_per_task_page = get_last_question_per_task_page_id(df_batch)
    path_batch = get_path_part(study,batch)
    save_batch_with_toloka_columns(df_batch,path_batch)

    path_formatted=get_path_part(study,batch+'-formatted')
    path_batch=get_path_part(study,batch)
    save_formmated_tasks(path_batch,path_formatted,last_question_id_per_task_page)


def get_last_question_per_task_page_id(df_batch):

    last_task_page_id=df_batch.iloc[0,df_batch.columns.get_loc('task-page-id')]
    last_question_id_per_task_page=[]
    last_index=None
    for index,row in df_batch.iterrows():
        if row['task-page-id']!=last_task_page_id:
            last_question_id=df_batch.loc[last_index,'question-id']
            last_task_page_id=row['task-page-id']
            last_question_id_per_task_page.append(last_question_id)
        last_index=index

    return last_question_id_per_task_page


def prepare_pilot_question_categories(study,is_production=True):
    initialize_logging(study)
    filter_on_topic_questions(study,is_production)
    filter_training_and_examples(study,is_production,20)
    generate_study_and_quality_checks(study,is_production)
    fitler_example_from_study(study,is_production)
    labels,batches=split_into_batches(study,2,is_production)
    task_page_size=20
    for batch in labels:

        is_added = add_quality_check(study,batch,0.1,task_page_size,is_production)
        if is_added:
            split_batch_into_task_pages(study,batch,task_page_size,is_production)
            add_examples(study,batch,is_production)
            format(study,batch)
        else:
            log_message("No Quality Checks for %s"%batch)



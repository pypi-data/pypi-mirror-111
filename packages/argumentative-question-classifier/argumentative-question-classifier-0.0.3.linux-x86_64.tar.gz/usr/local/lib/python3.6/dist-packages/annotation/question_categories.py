from conf.configuration import *
import logging
from datetime import datetime
import pandas as pd
from mylogging import *
import numpy as np
import os.path
import random
import math
import copy
from annotation.pilot_question_categories import *
from utils.pandas_util import *

task_page_size=10
quality_checks_ratio=0.1
annotation_count_per_page=9
group_topic_map={1:[18, 11], 2:[9, 10, 4, 3, 5, 14, 1, 15], 3:[8, 12, 2, 20, 21, 19, 13, 6], 4:[17, 7]} # key is a group, value is a list of topics
group_batch_map={1:[1, 2, 3, 4, 5, 6,7,8,101,102,103,104], 2:[9, 10, 11, 12, 13, 14, 15 ,109,110,111,112,113,114], 3:[16, 17, 18, 19, 20, 21,116,117], 4:[22, 23, 122, 123]} # key is a group, value is a list of batches
scheme={'factoid':0,'method':1,'argumentative':2,'opinion':3}
scheme_reversed={value:pretty for pretty,value in scheme.items()}
def load_topics():
    path_topic_described= get_path_described_topics('top-topics')
    df_topic_description=pd.read_csv(path_topic_described,sep="\t",encoding="utf-8")
    df_topic_description=df_topic_description[['topic','topic-id']]
    return df_topic_description

def drop_not_on_topic(study,is_production,log_paths):
    df_topics=load_topics()
    all_questions_to_annotate=0
    all_questions=0
    for group in range(1,5):
        log_message('dropping not on topic questions for group %d'%group)
        label_group_production="group-%d-production"%group
        label_group="group-%d"%group

        df_group=load_subdatset(study='topic-relevance',part=label_group_production,index_col=None,log=log_paths)
        df_group=df_group[["INPUT:id", "question","topic","annotation"]]
        df_group_on_topic=df_group[df_group['annotation']==0]
        df_group_no_on_topic=df_group[df_group['annotation']!=0]
        df_group_on_topic.rename(columns={'INPUT:id':'question-id'},inplace=True)
        df_group_on_topic=df_group_on_topic.merge(df_topics,on='topic')
        log_subtraction(label_group,df_group_on_topic,'topic-relevance:'+label_group_production,df_group,'not on topic',df_group_no_on_topic)
        df_group_on_topic=df_group_on_topic[["question-id","question","topic","topic-id"]]

        if group==2:
            df_group_on_topic_with_qc=df_group_on_topic.copy()
            df_deathpeanlty_quality_checks=sample_quality_checks_for_death_penalty(df_group_on_topic)
            df_group_on_topic=df_group_on_topic[~df_group_on_topic.index.isin(df_deathpeanlty_quality_checks.index)]
            log_subtraction(label_group,df_group_on_topic,label_group,df_group_on_topic_with_qc,'group-2-quality-checks-death-penalty',df_deathpeanlty_quality_checks)
            save_subdataset(study=study,part='group-2-quality-checks-death-penalty',subdataset=df_deathpeanlty_quality_checks,save_index=False,log=log_paths,check_existence=is_production)

        save_subdataset(study=study,part=label_group,subdataset=df_group_on_topic,save_index=False,log=log_paths,check_existence=is_production)
        #save_subdataset(study=study,part=label_group_remaining,subdataset=df_group_on_topic,save_index=False,log=log_paths,check_existence=is_production)
        all_questions=all_questions+df_group.shape[0]
        all_questions_to_annotate=all_questions_to_annotate+df_group_on_topic.shape[0]
    log_message(f"Study size {all_questions_to_annotate} from {all_questions}")

def add_not_annotated_questions(study,log_paths,is_production):
    label_group="group-2"
    df_group=load_subdatset(study=study,part=label_group,log=log_paths)
    _,df_death_penalty_question_to_annotate=integrate_death_penalty_quality_checks(study)
    df_group=pd.concat([df_group,df_death_penalty_question_to_annotate])
    save_subdataset(study=study,part=label_group,subdataset=df_group,save_index=True,log=log_paths,check_existence=is_production)

def change_training_scheme(is_production,log_paths):
    #looks like pilot study had not 'others' training?
    df_pilot_study_training=load_subdatset(study='pilot-question-categories',part='training-formatted',index_col=None,log=log_paths)
    del df_pilot_study_training['INPUT:example-others']
    save_subdataset(study='question-categories',part='training-formatted',subdataset=df_pilot_study_training,save_index=False,log=log_paths,check_existence=is_production)


def change_groundtruth_scheme(is_production,log_paths):
    log_message("chaning scheme from 4 to four")
    df_ground_truth=load_subdatset(study='pilot-question-categories',part='ground-truth',log=log_paths)
    df_ground_truth['annotation']=df_ground_truth['annotation'].apply(lambda annotation: 3 if (annotation == 4) else annotation)
    save_subdataset(study='question-categories',part='ground-truth',subdataset=df_ground_truth,log=True,check_existence=is_production)

def change_examples_scheme(is_production,log_paths):
    df_examples=load_subdatset(study='pilot-question-categories',part='examples',log=log_paths)
    df_training_examples=load_subdatset(study='pilot-question-categories',part='training-examples-to-add',log=log_paths)
    df_examples=df_examples[df_examples['annotation'].isin([0,1,2,3])]
    del df_training_examples['task-id']
    df_training_examples=df_training_examples[df_training_examples['annotation'].isin([0,1,2,3])]
    df_examples=pd.concat([df_examples, df_training_examples])
    save_subdataset(study='question-categories',part='examples',subdataset=df_examples,log=log_paths,check_existence=is_production)

def change_scheme(is_production,log_paths):
    change_training_scheme(is_production,log_paths)
    change_groundtruth_scheme(is_production,log_paths)
    change_examples_scheme(is_production,log_paths)

def sample_quality_checks_for_death_penalty(df_questions):
    df_death_penlty=df_questions[df_questions['topic-id']==3]
    df_death_penlty_quality_checks=df_death_penlty.sample(100)
    return df_death_penlty_quality_checks

def split_ground_truth_into_groups(study,is_production,log_paths):
    df_ground_truth=load_subdatset(study=study,part='ground-truth',log=log_paths)
    groups_quality_checks=[]
    gorups_quality_check_labels=[]
    for group in range(1,5):
        label_group_quality_checks='group-%d-quality-checks'%group
        group_topics=group_topic_map[group]
        df_group_ground_truth=df_ground_truth[df_ground_truth['topic-id'].isin(group_topics)]
        groups_quality_checks.append(df_group_ground_truth)
        gorups_quality_check_labels.append(label_group_quality_checks)
        if group == 2:
            df_death_penalty_quality_checks,_=integrate_death_penalty_quality_checks(study)
            df_group_ground_truth = pd.concat([df_group_ground_truth, df_death_penalty_quality_checks])

        save_subdataset(study=study,part=label_group_quality_checks,subdataset=df_group_ground_truth,log=log_paths,check_existence=is_production)
    log_split('ground-truth',df_ground_truth,gorups_quality_check_labels,groups_quality_checks,)

def prepare_question_categories(study,is_production=False,log_paths=False):
    initialize_logging(study)
    drop_not_on_topic(study,True,log_paths)
    change_scheme(is_production,log_paths)
    split_ground_truth_into_groups(study,is_production,log_paths)


def get_next_batch_id(study,group,is_production):

    batches=group_batch_map[group]
    if not is_production:
        return batches[0]
    for batch in batches:
        batch_label="batch-%d-source"%batch
        log_message(f"checking batch {batch}")
        if not subdataset_exists(study,batch_label):
            return batch

    raise ValueError(f"No batch found for group {group}")

def add_low_quality_to_remaining(study,group):
    label_gorup_result=f"group-{group}-results"
    path_group_results=get_path_part(study,label_gorup_result)
    df_group_results=pd.read_csv(path_group_results,sep="\t",encoding="utf-8")
    log_size(label_gorup_result,df_group_results)
    df_group_missing=df_group_results[df_group_results['high-all'].isna()]
    df_group_results=df_group_results[df_group_results['high-all']<3]

    log_size("missing",df_group_missing)
    log_size(label_gorup_result+"[high-all < 3]",df_group_results)
    df_group_to_be_annotated=df_group_results[['question-id','topic','topic-id','question']]
    df_group_missing=df_group_missing[['question-id','topic','topic-id','question']]
    df_group_to_be_annotated.set_index('question-id',inplace=True)
    df_group_missing.set_index('question-id',inplace=True)
    label_group_remaining="group-%d-remaining"%group
    df_group_remaining=load_subdatset(study,label_group_remaining)
    df_group_remaining=df_group_remaining[~df_group_remaining.index.isin(df_group_to_be_annotated.index)]
    df_group_remaining=pd.concat([df_group_remaining,df_group_to_be_annotated,df_group_missing])
    log_size(label_group_remaining,df_group_remaining)
    save_subdataset(study,label_group_remaining,df_group_remaining,check_existence=False)

def add_quality_checks(study,group,log_paths=False,is_production=False):


    log_message(f"adding group-{group} quality cehcks")
    label_gorup_result=f"group-{group}-results"
    path_group_results=get_path_part(study,label_gorup_result)
    df_group_results=pd.read_csv(path_group_results,sep="\t",encoding="utf-8",dtype={'annotation':pd.Int64Dtype(),'is-quality-check':pd.Int64Dtype()})
    if 'is-quality-check' in df_group_results.columns:
        df_new_quality_checks=df_group_results[df_group_results['is-quality-check']==1]
        log_size('new quality checks',df_new_quality_checks)

        df_new_quality_checks=df_new_quality_checks[['question-id','topic','topic-id','question','annotation']]
        df_new_quality_checks.set_index('question-id',inplace=True)
        label_group_quality_checks='group-%d-quality-checks'%group
        df_group_ground_truth=load_subdatset(study,label_group_quality_checks,index_col='question-id')

        log_size(label_group_quality_checks,df_group_ground_truth)
        df_group_ground_truth=df_group_ground_truth[~df_group_ground_truth.index.isin(df_new_quality_checks.index)]

        log_message("dropping existing quality checks\n")
        log_size(label_group_quality_checks,df_group_ground_truth)
        df_group_ground_truth=pd.concat([df_group_ground_truth, df_new_quality_checks])
        log_size(label_group_quality_checks,df_group_ground_truth)
        save_subdataset(study=study,part=label_group_quality_checks,subdataset=df_group_ground_truth,log=log_paths,check_existence=is_production)
    else:
        log_message(f"no quality check in group-{group}")

def get_pool_sampling_for(study, batch):
    path_batches = get_path_batches(study)
    df_batches = pd.read_csv(path_batches,sep=",",encoding="utf-8")
    sampling_strategy = df_batches.loc[df_batches['batch']==batch,'pool-sampling'].iloc[0]
    return sampling_strategy


def sample_batch(study, group,batch, quality_checks_per_topic, is_production,log_paths):
    label_batch="batch-%d-source"%batch
    label_group_remaining="group-%d-remaining"%group

    if subdataset_exists(study,label_group_remaining):
        label_group_source=label_group_remaining
    else:
        label_group_source="group-%d"%group
    df_group=load_subdatset(study=study,part=label_group_source,log=log_paths)
    if df_group.empty:
        return pd.DataFrame({})
    batch=[]
    for topic_id, questions_per_topic in list(df_group.groupby('topic-id')):
        if topic_id in quality_checks_per_topic:
            quality_checks_topic= quality_checks_per_topic[topic_id]
        topic_sample_size=quality_checks_topic*annotation_count_per_page
        if topic_sample_size<questions_per_topic.shape[0]:
            sampled_questions=questions_per_topic.sample(n=topic_sample_size)
        else:
            sampled_questions=questions_per_topic
        batch.append(sampled_questions)
    df_batch=pd.concat(batch)
    log_sample(label_batch,df_batch,label_group_source,df_group,(df_batch.shape[0]/df_group.shape[0]*100))
    df_group_source=df_group.copy()
    df_group=df_group[~df_group.index.isin(df_batch.index)]

    log_subtraction(label_group_remaining,df_group,label_group_source,df_group_source,label_batch,df_batch)
    save_subdataset(study,label_batch,df_batch,log=log_paths,check_existence=is_production)
    save_subdataset(study,label_group_remaining,df_group,log=log_paths,check_existence=False)
    return df_batch

def load_quality_checks(study,group):
    label_group_quality_checks='group-%d-quality-checks'%group
    return load_subdatset(study,label_group_quality_checks)

def filter_group_results(df_group_results,batch):
    for batch_iteration in range(0,4):
        df_group_results=df_group_results[df_group_results[f'batch-{batch_iteration}']==batch]
        if(df_group_results.shape[0]>0):
            return df_group_results
    raise ValueError(f"Batch{batch} not processed yet")
def load_quality_checks_for_batch(study,group,batch):
    batches=group_batch_map[group]
    if batch == batches[0]:
        label_group_quality_checks='group-%d-quality-checks'%group
        return load_subdatset(study,label_group_quality_checks)
    else:
        index = batches.index(batch)
        last_batch=batches[index-1]
        label_group_result="group-%d-results"%group
        path_group_results=get_path_part(study,label_group_result)
        df_group_results=pd.read_csv(path_group_results,sep="\t")
        df_batch=filter_group_results(df_group_results,last_batch)
        df_batch=df_batch[df_batch['is-quality-check']==1]
        df_batch=df_batch[['question-id','question','topic','topic-id','annotation']]
        df_batch.set_index('question-id',inplace=True)
        return df_batch,last_batch


def get_maximum_annotation_size(df_annotation_per_topic):
    return sum(sorted(df_annotation_per_topic['annotation'].value_counts().values)[:-1])

def get_quality_checks_per_topic(df_quality_checks):
    return df_quality_checks['topic-id'].value_counts().to_dict()

def formate_annotation_type_counts(non_factoid_quality_checks):
    annotation_type_counts=non_factoid_quality_checks['annotation'].value_counts().to_dict()
    annotation_type_counts_pretty={scheme_reversed[annotation_type]:count for annotation_type,count in annotation_type_counts.items()}
    annotation_type_counts_pretty_formatted=[f"{annotation_count:>4} {annotation:>14}" for annotation,annotation_count in sorted(annotation_type_counts_pretty.items())]
    return   " ".join(annotation_type_counts_pretty_formatted)

def sample_quality_checks(study,group,batch,from_pool,is_production,log_paths):
    label_batch_quality_checks="batch-%d-quality-checks"%batch
    if from_pool:

        df_quality_checks=load_quality_checks(study,group)
        log_message(f"sampling quality checks for batch {batch} from pool[{df_quality_checks.shape[0]}]")
    else:
        df_quality_checks,last_batch=load_quality_checks_for_batch(study,group,batch)
        log_message(f"sampling quality checks for batch {batch} from previous batch-{last_batch}[{df_quality_checks.shape[0]}]")
    quality_checks=[]
    for topic_id, quality_checks_per_topic in  list(df_quality_checks.groupby('topic-id')):
        factoid_quality_checks_size=get_maximum_annotation_size(quality_checks_per_topic)
        all_factoid_quality_checks=quality_checks_per_topic[quality_checks_per_topic['annotation']==0]
        non_factoid_quality_checks=quality_checks_per_topic[quality_checks_per_topic['annotation']!=0]
        factoid_quality_checks=all_factoid_quality_checks.sample(factoid_quality_checks_size)
        non_factoid_formated=formate_annotation_type_counts(non_factoid_quality_checks)
        topic_quality_checks=non_factoid_quality_checks.shape[0]+factoid_quality_checks.shape[0]
        log_message(f"{topic_quality_checks } quality checks for topic {topic_id:<3} ->{factoid_quality_checks.shape[0]:>4} factoid "+ non_factoid_formated)
        quality_checks.append(factoid_quality_checks)
        quality_checks.append(non_factoid_quality_checks)

    df_batch_quality_checks= pd.concat(quality_checks)
    log_message(f"{df_batch_quality_checks.shape[0]} quality checks for batch {batch}\n")
    save_subdataset(study=study,part=label_batch_quality_checks,subdataset=df_batch_quality_checks,log=log_paths,check_existence=is_production)
    return  df_batch_quality_checks







def split_batch_into_task_pages(study,batch,df_batch,df_batch_quality_checks,is_production,log_paths):
    task_page_id=0
    task_pages_with_quality_checks=[]
    for topic_id,topic_questions in list(df_batch.groupby('topic-id')):
        topic_questions_size=topic_questions.shape[0]

        if topic_questions_size%annotation_count_per_page==0:
            count_of_taskpages=topic_questions_size/annotation_count_per_page
        else:
            count_of_taskpages=int(topic_questions_size/annotation_count_per_page)+1
        log_message(f"{int(count_of_taskpages):>3} taskpages for topic {topic_id:>2}")
        task_pages=np.array_split(topic_questions,count_of_taskpages)
        df_topic_quality_checks=df_batch_quality_checks[df_batch_quality_checks['topic-id']==topic_id]
        df_topic_quality_checks=df_topic_quality_checks.sample(frac=1)


        for i,task_page in enumerate(task_pages):

            task_page['annotation']=""
            if df_topic_quality_checks.shape[0]==0:
                continue
            else:
                task_page=task_page.append(df_topic_quality_checks.iloc[i,:])
            task_page['task-page-id']=task_page_id
            task_page_id=task_page_id+1
            task_page=task_page.sample(frac=1).reset_index()

            task_pages_with_quality_checks.append(task_page)
    log_message(f"{len(task_pages_with_quality_checks):>3} taskpages for batch {batch:>2} \n")
    df_batch_split=pd.concat(task_pages_with_quality_checks)
    label_batch_split="batch-%d-split"%batch
    label_batch="batch-%d"%batch
    label_batch_quality_checks="batch-%d-quality-checks"%batch
    log_addition(label_batch_split,df_batch_split,label_batch,df_batch,label_batch_quality_checks,df_batch_quality_checks)
    save_subdataset(study=study,part=label_batch_split,subdataset=df_batch_split,save_index=False,log=log_paths,check_existence=is_production,)
    df_batch_split.set_index('question-id',inplace=True)
    return df_batch_split


def add_examples(study,batch,df_batch_split,is_production,log_paths):

    label_batch="batch-%d"%batch
    label_batch_examples="batch-%d-examples"%batch
    def rename_columns(df_examples):

        df_examples.rename(columns={0:'example-fact',1:'example-method',2:'example-argument',3:'example-opinion'},inplace=True)
        df_examples['question']='question'
        df_examples['question-id']=-1
        df_examples['topic']=topic
        df_examples['topic-id']=topic_id
        df_examples['task-page-id']=task_page_id
        df_examples.set_index('question-id',inplace=True)

    def add_example_columns(df_batch):
        for label in ['fact','method','argument','opinion']:
            df_batch['example-'+label]='example-'+label


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

    save_subdataset(study,label_batch_examples,df_batch_with_examples,check_existence=is_production,log=log_paths)
    log_addition(label_batch_examples,df_batch_with_examples,label_batch+'-split',df_batch_split,'examples',df_batch_examples)


def save_batch_with_toloka_columns(df_batch,path_batch):
    df_batch = df_batch[['question','question-id','task-id','annotation','example-fact', \
                         'example-method','example-opinion','example-argument']].rename(
        columns={'question-id':"INPUT:id",'task-id':"INPUT:task-id","question":"INPUT:question","annotation":"GOLDEN:category"
            ,"example-fact":"INPUT:example-fact","example-method":"INPUT:example-method","example-opinion":"INPUT:example-opinion",
                 'example-argument':"INPUT:example-argument"
                 })
    df_batch['GOLDEN:category']=df_batch['GOLDEN:category'].fillna(-1).astype(int)
    df_batch['GOLDEN:category'].loc[df_batch['GOLDEN:category']==-1]=""

    df_batch.to_csv(path_or_buf=path_batch,sep="\t",encoding="utf-8",columns=['INPUT:id','INPUT:question','INPUT:example-fact','INPUT:example-method','INPUT:example-argument','INPUT:example-opinion',"INPUT:task-id",'GOLDEN:category'],index=False)

def save_formmated_tasks(path_batch_final,path_batch_formatted,last_question_id_per_task_page):
    skip_header=False
    count_of_lines=0
    size_of_batch=pd.read_csv(path_batch_final,sep="\t",encoding="utf-8").shape[0]
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
    logging.warning(f"batch-fromatted      [{count_of_lines}]    <-  batch[{size_of_batch}]")


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


def generate_batch(study,group,is_production,log_paths):
    initialize_logging(study)
    try:
        batch=get_next_batch_id(study,group,is_production)
    except ValueError as error:
        log_message(error)
        return
    log_message(f"generating batch {batch}")
    pool_sampling = get_pool_sampling_for(study,batch)
    df_batch_quality_checks = sample_quality_checks(study,group,batch,pool_sampling,is_production,log_paths)
    quality_checks_per_topic = get_quality_checks_per_topic(df_batch_quality_checks)
    df_batch=sample_batch(study,group,batch,quality_checks_per_topic,is_production,log_paths)
    if df_batch.empty:
        log_message(f"group {group} is done !")
    else:
        df_batch_split=split_batch_into_task_pages(study,batch,df_batch,df_batch_quality_checks,is_production,log_paths)
        add_examples(study,batch,df_batch_split,is_production,log_paths)
        format(study,"batch-%d"%batch)




def integrate_death_penalty_quality_checks(study):
    label_group_quality_checks='group-2-quality-checks-death-penalty'
    df_death_penalty_quality_checks=load_subdatset(study,label_group_quality_checks)
    df_death_penalty_quality_checks['annotation']=-1

    for index,death_penalty_question in df_death_penalty_quality_checks.iterrows():
        for annotation_type in scheme:
            if death_penalty_question[annotation_type] == 1:
                df_death_penalty_quality_checks.loc[index,'annotation']=scheme[annotation_type]
    del df_death_penalty_quality_checks['factoid']
    del df_death_penalty_quality_checks['method']
    del df_death_penalty_quality_checks['argumentative']
    del df_death_penalty_quality_checks['opinion']
    del df_death_penalty_quality_checks['not question']
    del df_death_penalty_quality_checks['not on topic']

    df_questions_to_annotate=df_death_penalty_quality_checks[df_death_penalty_quality_checks['annotation']==-1]
    df_quality_checks=df_death_penalty_quality_checks[df_death_penalty_quality_checks['annotation']!=-1]
    del df_questions_to_annotate['annotation']
    return df_quality_checks, df_questions_to_annotate


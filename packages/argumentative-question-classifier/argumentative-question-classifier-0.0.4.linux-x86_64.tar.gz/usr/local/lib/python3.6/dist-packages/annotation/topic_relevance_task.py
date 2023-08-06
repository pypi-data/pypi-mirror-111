from conf.configuration import *
import pandas as pd
import numpy as np
import logging
import random
import os.path
pd.options.mode.chained_assignment=None
task_page_size=18

group_topic_map={1:[18, 11], 2:[9, 10, 4, 3, 5, 14, 1, 15], 3:[8, 12, 2, 20, 21, 19, 13, 6], 4:[17, 7]} # key is a group, value is a list of topics
group_batch_map={1:[1, 2, 3, 4, 5, 6], 2:[9, 10, 11, 12, 13, 14, 15 , 24], 3:[16, 17, 18, 19, 20, 21,7,8], 4:[22, 23]} # key is a group, value is a list of batches
group_batch_map_2nd_iter={1:[101, 102, 103], 2:[109, 110, 111], 3:[116, 117, 118], 4:[122, 123, 124]}
bathces_2nd_iter_final=[group_batch_map_2nd_iter[group][-1] for group in group_batch_map_2nd_iter]
min_num_questions_per_topic=1000 * task_page_size
max_batch_size=13600

path_log=get_path_log('topic-relevance')

logging.basicConfig(filename=path_log,level=logging.DEBUG,format='%(message)s')

def load_batch(batch,dataset):
    label_batch = "batch-%d-source"%batch
    path_batch_study=get_path_part(dataset,label_batch)
    df_batch = pd.read_csv(path_batch_study,sep="\t",encoding="utf-8")
    path_top_topics_translated=get_path_described_topics('top-topics')
    df_top_topics_translated=pd.read_csv(path_top_topics_translated,sep='\t',encoding="utf-8")
    df_top_topics_translated['topic']=df_top_topics_translated['topic'].astype(str)
    df_batch=df_batch.merge(df_top_topics_translated[['topic','topic-id']],on='topic',how='left')
    df_batch.rename(columns={'INPUT:id':'question-id'},inplace=True)
    return df_batch

def get_group_for_batch(batch):

    for group in group_batch_map:
        if batch in group_batch_map[group]:
            return group
        if batch in group_batch_map_2nd_iter[group]:
            return group


def generate_groups(df_study):
    logging.warning("study[%d] -> "%df_study.shape[0])
    for group in group_topic_map:
        topics = group_topic_map[group]
        df_group = df_study[df_study['topic-id'].isin(topics)]
        logging.warning("group-%d[%d] -> "%(group,df_group.shape[0]))
        label_group="group-%d"%group
        path_group=get_path_part('topic-relevance', label_group)
        df_group.to_csv(path_group,sep="\t",encoding="utf-8")

def get_next_batch_to_generate(group):
    batches = group_batch_map[group]
    last_generated_batch=batches[0]
    previous_batch=None
    for i,batch in enumerate(batches):
        batch_source_label='batch-%d-source'%(batch)
        if os.path.exists(get_path_part('topic-relevance', batch_source_label)):
            previous_batch=batch
            if i+1 < len(batches):
                last_generated_batch=batches[i+1]
            else:
                last_generated_batch=None

    if last_generated_batch!=None:
        last_done_batch=get_last_done_batch_per_group(group)
        if previous_batch!=last_done_batch:
            return last_generated_batch,previous_batch
    return last_generated_batch,None

def get_last_done_batch_per_group(group):
    batches = group_batch_map[group]
    last_done_batch=None
    for batch in batches:
        batch_agreed_label='batch-%d-agreed'%(batch)
        if os.path.exists(get_path_part('topic-relevance', batch_agreed_label)):
            last_done_batch=batch
    return last_done_batch

def get_hints():
    hints = {}
    hints[0]= 'вопрос относится к данной теме'
    hints[1]= 'не по теме: вопрос не связан с данной темой.'
    hints[2]= 'не вопрос: представленный текст не является вопросом.'
    return hints

def get_topic_distribution(group):
    topic_distribution={}

    label_group="group-%d"%group
    path_group=get_path_part('topic-relevance', label_group)
    label_group_remaning="group-%d-remaining"%group
    path_group_remaining=get_path_part('topic-relevance', label_group_remaning)
    if os.path.exists(path_group_remaining):
        df_group=pd.read_csv(path_group_remaining,sep="\t",encoding="utf-8")
    else:
        df_group=pd.read_csv(path_group,sep="\t",encoding="utf-8")
    num_of_questions=df_group.shape[0]
    for topic, df_topic_questions in df_group.groupby('topic-id'):
        topic_distribution[topic]=df_topic_questions.shape[0]/num_of_questions

    return topic_distribution

def estimate_size_of_batch(df_group_quality_checks,topic_distribution):

    num_of_quality_checks_per_topic={}
    count_questions_per_topic= {}
    for topic, df_topic_quality_checks in df_group_quality_checks.groupby('topic-id'):
        logging.warning("estimating size for topic %d"%topic)
        topic_ratio=0
        if topic in topic_distribution:
            topic_ratio= topic_distribution[topic]
        max_num_questions_per_topic= max_batch_size * topic_ratio
        logging.warning("min #questions per topic is %d; max #questions per topic is %d"%(min_num_questions_per_topic,max_num_questions_per_topic))
        z_t=df_topic_quality_checks[df_topic_quality_checks['annotation']==1].shape[0]
        num_of_quality_checks_per_topic[topic] = z_t*2
        logging.warning("original size estimate for topic %d is %d "%(topic,num_of_quality_checks_per_topic[topic] * 9))
        if num_of_quality_checks_per_topic[topic] * 9 < min_num_questions_per_topic:
            num_of_quality_checks_per_topic[topic]=int(min_num_questions_per_topic/9)
            logging.warning("min is taken")
        count_questions_per_topic[topic]=num_of_quality_checks_per_topic[topic]*9
        logging.warning("#questions for topic %d is %d"%(topic,count_questions_per_topic[topic]))
        if count_questions_per_topic[topic]>max_num_questions_per_topic:
            count_questions_per_topic[topic]=max_num_questions_per_topic
            logging.warning("max is taken")
    return count_questions_per_topic,num_of_quality_checks_per_topic

def generate_batches():
    generated_batches=[]


    for group in group_topic_map:
        label_group_remaning="group-%d-remaining"%group
        path_group_remaining=get_path_part('topic-relevance', label_group_remaning)
        if os.path.exists(path_group_remaining):
            df_group_remaining=pd.read_csv(path_group_remaining,sep="\t",encoding="utf-8")
            if df_group_remaining.shape[0]==0:
                continue
        topic_distribution=get_topic_distribution(group)
        logging.warning("topic ratio for group %s"%group)
        for topic_id in topic_distribution:
            logging.warning("topic %d is %2.2f"%(topic_id,topic_distribution[topic_id]))
        label_group_quality_checks='group-%d-quality-checks'%group
        path_group_quality_checks=get_path_part('topic-relevance', label_group_quality_checks)
        df_group_quality_checks=pd.read_csv(path_group_quality_checks,sep="\t",encoding="utf-8")
        batch_id,previous_batch=get_next_batch_to_generate(group)
        all_topics_questions=[]
        if batch_id!=None:
            is_first_batch= batch_id == group_batch_map[group][0]
            if previous_batch!=None:
                logging.warning("next batch for group %d is %d; however, %d is in progress"%(group,batch_id,previous_batch))
                continue
            else:
                label_group="group-%d"%group
                path_group=get_path_part('topic-relevance', label_group)
                if is_first_batch:
                    df_group=pd.read_csv(path_group,sep="\t",encoding="utf-8",index_col='question-id')
                    logging.warning("group-%d[%d]-> "%(group,df_group.shape[0]))
                    logging.warning("generating the first batch")
                else:
                    df_group=pd.read_csv(path_group_remaining,sep="\t",encoding="utf-8",index_col='question-id')
                    logging.warning("group-%d-remaining[%d]-> "%(group,df_group.shape[0]))

                count_questions_per_topic,num_of_quality_checks_per_topic=estimate_size_of_batch(df_group_quality_checks,topic_distribution)

                batch_source_label='batch-%d-source'%(batch_id)
                path_source_batch= get_path_part('topic-relevance', batch_source_label)
                for topic_id, topic_questions in df_group.groupby('topic-id'):
                    count_of_rest_questions_per_topic=topic_questions.shape[0]
                    if count_questions_per_topic[topic_id]< count_of_rest_questions_per_topic:
                        topic_questions_sample=topic_questions.sample(int(count_questions_per_topic[topic_id]))
                    else:
                        topic_questions_sample=topic_questions
                    all_topics_questions.append(topic_questions_sample)
                df_batch=pd.concat(all_topics_questions)

                df_batch.to_csv(path_source_batch,sep="\t",encoding="utf-8",index='question-id')
                logging.warning("batch-%d[%d] saved"%(batch_id,df_batch.shape[0]))
                df_group_remaining=df_group[~df_group.index.isin(df_batch.index)]
                df_group_remaining.to_csv(path_group_remaining,sep="\t",encoding="utf-8",index='question-id')
                logging.warning("group-%d-remaining[%d] saved"%(group,df_group_remaining.shape[0]))
                generated_batches.append(batch_id)
        else:
            logging.warning("all batches are done for group %d"%group)
    return generated_batches

def split_batch_into_taskpages(df_batch,task_page_size):
    task_page_id=0
    all_df_task_pages=[]
    for _ ,df_topic_questions in df_batch.groupby('topic-id'):
        num_task_pages= df_topic_questions.shape[0]/ task_page_size
        if num_task_pages<1:
            num_task_pages=1
        dfs_task_pages = np.array_split(df_topic_questions,num_task_pages)
        for df_task_page in dfs_task_pages:
            df_task_page['task-page-id']=task_page_id
            task_page_id=task_page_id+1
        all_df_task_pages.extend(dfs_task_pages)
    df_batch_with_task_pages=pd.concat(all_df_task_pages)
    return df_batch_with_task_pages

def split_quality_checks_into_groups(df_quality_checks):
    df_quality_checks.reset_index(inplace=True)
    path_top_topics_translated=get_path_described_topics('top-topics')
    df_top_topics_translated=pd.read_csv(path_top_topics_translated,sep='\t',encoding="utf-8")
    df_top_topics_translated['topic']=df_top_topics_translated['topic'].astype(str)
    df_quality_checks['topic']=df_quality_checks['topic'].astype(str)
    df_quality_checks=df_quality_checks.merge(df_top_topics_translated[['topic','topic-id']],on='topic',how='left')
    logging.warning("ground-truth-without-training[%d] -> "%df_quality_checks.shape[0])
    for group in group_topic_map:
        label_group_quality_checks='group-%d-quality-checks'%group
        topics=group_topic_map[group]
        df_group_quality_checks=df_quality_checks[df_quality_checks['topic-id'].isin(topics)]
        path_group_quality_checks=get_path_part('topic-relevance', label_group_quality_checks)
        if (path_group_quality_checks):
            logging.warning("%s[%d] saved covering topics %s"%(label_group_quality_checks,df_group_quality_checks.shape[0],str(topics)))
        else:
            logging.warning("%s is wrongly written"%label_group_quality_checks)
        df_group_quality_checks.to_csv(path_group_quality_checks,sep="\t",encoding="utf-8",index=False)

def generate_batch_quality_checks(batch_id,dataset):

    group=get_group_for_batch(batch_id)
    label_group='group-%d-quality-checks'%group
    path_group_quality_checks=get_path_part('topic-relevance', label_group)
    df_quality_checks_source =pd.read_csv(path_group_quality_checks,sep="\t",encoding="utf-8",index_col="question-id")
    batch_label="batch-%d"%(batch_id)+'-split'
    path_batch_splitted=get_path_part(dataset, batch_label)
    path_batch_with_quality_checks=get_path_part(dataset, 'batch-%d-quality-checks' % batch_id)
    df_splitted_batch=pd.read_csv(path_batch_splitted,sep="\t",encoding="utf-8",index_col="question-id")
    df_batch_quality_checks=pd.DataFrame({})
    for topic_id, topic_questions in df_splitted_batch.groupby('topic-id'):

        task_page_ids=topic_questions['task-page-id'].values
        unique_task_page_ids=list(set(task_page_ids))
        num_task_pages = len(unique_task_page_ids)
        df_topic_quality_checks=df_quality_checks_source[df_quality_checks_source['topic-id']==topic_id]
        df_on_topic_quality_checks= df_topic_quality_checks[df_topic_quality_checks['annotation']==0].sample(num_task_pages)
        df_not_on_topic_questions=df_topic_quality_checks[df_topic_quality_checks['annotation']==1]
        if df_not_on_topic_questions.shape[0]<num_task_pages:
            df_not_on_topic_quality_checks=df_not_on_topic_questions
            df_not_on_topic_quality_checks['task-page-id']=np.random.choice(unique_task_page_ids,df_not_on_topic_quality_checks.shape[0],False)
        else:
            df_not_on_topic_quality_checks=df_not_on_topic_questions.sample(num_task_pages)
            df_not_on_topic_quality_checks['task-page-id']=unique_task_page_ids



        df_not_questions=df_topic_quality_checks[df_topic_quality_checks['annotation']==2]
        if df_not_questions.shape[0]<num_task_pages:
            df_not_a_question_quality_checks=df_not_questions
            df_not_a_question_quality_checks['task-page-id']=np.random.choice(unique_task_page_ids,df_not_a_question_quality_checks.shape[0],False)
        else:
            df_not_a_question_quality_checks=df_not_questions.sample(num_task_pages)
            df_not_a_question_quality_checks['task-page-id']=unique_task_page_ids



        df_on_topic_quality_checks['task-page-id']=unique_task_page_ids
        df_not_a_question_quality_checks['task-page-id']=np.random.choice(task_page_ids,df_not_a_question_quality_checks.shape[0])
        logging.warning("count of task pages for topic %d is "%(topic_id) + str(len(unique_task_page_ids)))
        logging.warning("batch %d - topic %d on topic quality checks is %d"%(batch_id,topic_id,df_on_topic_quality_checks.shape[0]))
        logging.warning("batch %d - topic %d not on topic quality checks is %d"%(batch_id,topic_id,df_not_on_topic_quality_checks.shape[0]))
        logging.warning("batch %d - topic %d not a question quality checks is %d"%(batch_id,topic_id,df_not_a_question_quality_checks.shape[0]))
        df_batch_quality_checks=pd.concat([df_batch_quality_checks,df_on_topic_quality_checks,df_not_on_topic_quality_checks,df_not_a_question_quality_checks])


    df_batch_with_quality_checks=pd.concat([df_splitted_batch,df_batch_quality_checks])
    df_batch_with_quality_checks=df_batch_with_quality_checks.sample(frac=1)
    logging.warning("split-with-quality-checks[%d] <- "%df_batch_with_quality_checks.shape[0]+ "quality-checks[%d] + "%df_batch_quality_checks.shape[0]+batch_label+"[%d]"%df_splitted_batch.shape[0])
    df_batch_with_quality_checks.to_csv(path_batch_with_quality_checks,sep="\t",encoding="utf-8")
    return df_batch_with_quality_checks

def fill_empty_columns(dataframe):

    dataframe['Russian-description']="description"
    dataframe['on-topic-example']="on-topic-example"
    dataframe['not-on-topic-example']="not-on-topic-example"
    dataframe['not-a-question-example']="not-a-question-example"

def fill_topic_description_empty_columns(df_topic_description):
    df_topic_description['question-id']=-1
    df_topic_description['question']="question"
    df_topic_description['annotation']=-1
    df_topic_description['hint']="hint"
    df_topic_description['task-id']=-1

def replicate_over_task_pages(df_topic_descriptions,df_batch):
    topics = df_batch['topic'].unique()
    all_task_topic_descriptions=[]

    for topic in topics:
        df_topic_questions= df_batch[df_batch['topic']==topic]
        task_page_ids=df_topic_questions['task-page-id'].unique()
        for task_page_id in task_page_ids:
            topic_description=df_topic_descriptions[df_topic_descriptions['topic']==topic]
            topic_description['task-page-id']=task_page_id
            all_task_topic_descriptions.append(topic_description)
    return pd.concat(all_task_topic_descriptions)

def get_topic_description(df_batch):
    path_top_topics_described=get_path_described_topics('top-topics')
    df_topic_description=pd.read_csv(path_top_topics_described,sep='\t',encoding="utf-8")
    df_topic_description=df_topic_description[['topic-id','topic','Russian-description']]
    df_topic_description=df_topic_description[(df_topic_description['topic-id']!=8) & (df_topic_description['topic-id']!=16)]
    topics = df_batch['topic-id'].unique()
    df_topic_description=df_topic_description[df_topic_description['topic-id'].isin(topics)]
    fill_topic_description_empty_columns(df_topic_description)
    df_examples =load_examples()

    for index, row in df_topic_description.iterrows():
        topic = row['topic']
        on_topic_question_example=df_examples.loc[(df_examples['topic']==topic) & (df_examples['annotation'] ==0),'question'].values[0]
        not_on_topic_question_example=df_examples.loc[(df_examples['topic']==topic) & (df_examples['annotation'] ==1),'question'].values[0]
        not_a_question_example=df_examples.loc[(df_examples['topic']==topic) & (df_examples['annotation'] ==2),'question'].values[0]

        df_topic_description.loc[index,'on-topic-example']=on_topic_question_example
        df_topic_description.loc[index,'not-on-topic-example']=not_on_topic_question_example
        df_topic_description.loc[index,'not-a-question-example']=not_a_question_example

    df_all_task_topic_descriptions=replicate_over_task_pages(df_topic_description,df_batch)
    logging.warning("topic-descriptions[%d]"%df_all_task_topic_descriptions.shape[0])
    return df_all_task_topic_descriptions

def load_examples():
    path_examples=get_path_part('topic-relevance', 'examples')
    df_examples = pd.read_csv(path_examples,sep="\t",encoding="utf-8")
    return df_examples

def get_last_question_per_task_page_id(df_batch):
    df_batch['temp-index']=df_batch.apply(lambda row: row['question-id']>0,axis=1)
    df_batch.sort_values(['topic','task-page-id','temp-index'],inplace=True)

    last_task_page_id=df_batch.iloc[0,df_batch.columns.get_loc('task-page-id')]
    last_question_id_per_task_page=[]
    last_index=None
    for index,row in df_batch.iterrows():
        if row['task-page-id']!=last_task_page_id:
            last_question_id=df_batch.loc[last_index,'question-id']
            last_task_page_id=row['task-page-id']
            last_question_id_per_task_page.append(last_question_id)
        last_index=index
    del df_batch['temp-index']
    return last_question_id_per_task_page

def analyze_per_topic_annotations(df_quality_checks_without_examples):
    path_top_topics_translated=get_path_described_topics('top-topics')
    df_top_topics_translated=pd.read_csv(path_top_topics_translated,sep='\t',encoding="utf-8")
    df_top_topics_translated['topic']=df_top_topics_translated['topic'].astype(str)
    df_quality_checks=df_quality_checks_without_examples.merge(df_top_topics_translated[['topic','topic-id']],on='topic',how='left')
    for topic_id, quality_checks_with_topic in df_quality_checks.groupby('topic-id'):
        num_of_not_on_topic_quality_checks=quality_checks_with_topic[quality_checks_with_topic['annotation']==1].shape[0]
        logging.warning("Num of not on topic quality checks for topic %d is %d"%(topic_id,num_of_not_on_topic_quality_checks))






def save_formmated_tasks(path_batch_final,path_batch_formatted,last_question_id_per_topic):
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
                if int(question_id) in list(last_question_id_per_topic):
                    file_annotation_tasks_batches.write(line+"\n")
                    count_of_lines=count_of_lines+1
                else:
                    file_annotation_tasks_batches.write(line)
                count_of_lines=count_of_lines+1
    logging.warning("batch-fromatted[%d] <- batch[%d]"%(count_of_lines,pd.read_csv(path_batch_final,sep="\t",encoding="utf-8").shape[0]))

def save_batch_with_toloka_columns(df_batch_with_examples,path_batch):
    df_batch_with_examples = df_batch_with_examples[['question','question-id','task-id','Russian-description','annotation','on-topic-example','not-on-topic-example','not-a-question-example']].rename(
        columns={'question-id':"INPUT:id",'task-id':"INPUT:task-id","question":"INPUT:question","Russian-description":"INPUT:topic-description","annotation":"GOLDEN:category"
            ,"on-topic-example":"INPUT:on-topic-example","not-on-topic-example":"INPUT:not-on-topic-example","not-a-question-example":"INPUT:not-a-question-example"
                 })
    df_batch_with_examples['GOLDEN:category']=df_batch_with_examples['GOLDEN:category'].fillna(-1).astype(int)
    df_batch_with_examples['GOLDEN:category'].loc[df_batch_with_examples['GOLDEN:category']==-1]=""
    df_batch_with_examples.to_csv(path_or_buf=path_batch,sep="\t",encoding="utf-8",columns=['INPUT:id','INPUT:question','INPUT:topic-description','INPUT:on-topic-example','INPUT:not-on-topic-example','INPUT:not-a-question-example',"INPUT:task-id",'GOLDEN:category'],index=False)

def save_batch_with_toloka_columns_training(df_batch_with_examples,path_batch):

    df_batch_with_examples = df_batch_with_examples[['question','question-id','task-id','Russian-description','annotation','on-topic-example','not-on-topic-example','not-a-question-example','hint']].rename(
        columns={'question-id':"INPUT:id","question":"INPUT:question","Russian-description":"INPUT:topic-description","annotation":"GOLDEN:category"
            ,"on-topic-example":"INPUT:on-topic-example",'task-id':"INPUT:task-id","not-on-topic-example":"INPUT:not-on-topic-example","not-a-question-example":"INPUT:not-a-question-example","hint":"HINT:text"
                 })
    df_batch_with_examples.to_csv(path_or_buf=path_batch,sep="\t",encoding="utf-8",columns=['INPUT:id','INPUT:question','INPUT:topic-description','INPUT:on-topic-example','INPUT:not-on-topic-example',"HINT:text",'INPUT:not-a-question-example',"INPUT:task-id",'GOLDEN:category'],index=False)

def add_hints_for_examples(df_examples):
    hints = get_hints()
    df_examples['hint']=df_examples.apply(lambda question: hints[int(question['annotation'])],axis=1)

def generate_study_questions():

    path_preprocessed_1= get_preprocessed_path('topic-relevance',1)
    path_preprocessed_2 = get_preprocessed_path('topic-relevance',2)
    path_preprocessed_3= get_preprocessed_path('topic-relevance',3)
    path_ground_truth=get_path_part('topic-relevance', 'ground-truth')
    path_examples=get_path_part('topic-relevance', 'examples')
    path_training_source = get_path_part('topic-relevance', 'training-source')
    df_training= pd.read_csv(path_training_source,sep="\t",encoding="utf-8",index_col="question-id")
    path_quality_checks_without_examples=get_path_part('topic-relevance', 'ground-truth-without-examples')
    path_study = get_path_part('topic-relevance', 'study')
    df_examples = pd.read_csv(path_examples,sep="\t",encoding="utf-8",index_col="question-id",dtype={'topic-id':int})
    df_quality_checks = pd.read_csv(path_ground_truth,sep="\t",encoding="utf-8",index_col="question-id",dtype={'topic-id':int,'annotation':int})
    df_quality_checks_without_examples=df_quality_checks[~df_quality_checks.index.isin(df_examples.index)]
    analyze_per_topic_annotations(df_quality_checks_without_examples)
    df_quality_checks_without_examples.to_csv(path_quality_checks_without_examples,sep="\t",encoding="utf-8")
    logging.warning("ground-truth-without-examples[%d] <- ground-truth[%d] - examples[%d]"%(df_quality_checks_without_examples.shape[0],df_quality_checks.shape[0],df_examples.shape[0]))
    df_quality_checks_without_training = df_quality_checks_without_examples[~df_quality_checks_without_examples.index.isin(df_training.index)]
    logging.warning("ground-truth-without-training[%d] <- ground-truth-without-examples[%d] - training[%d]"%(df_quality_checks_without_training.shape[0],df_quality_checks_without_examples.shape[0],df_training.shape[0]))
    split_quality_checks_into_groups(df_quality_checks_without_training)
    df_source = pd.read_csv(path_preprocessed_1,sep="\t",encoding="utf-8",index_col='question-id',dtype={'topic-id':int})
    df_source_without_duplicates=df_source.drop_duplicates('question')
    df_source_without_duplicates.to_csv(path_preprocessed_2,sep="\t",encoding="utf-8")
    logging.warning("preprocessed-2[%d] <- source[%d] - duplicates"%(df_source_without_duplicates.shape[0],df_source.shape[0]))
    df_source_without_animal_rights = df_source_without_duplicates[df_source_without_duplicates['topic-id']!=8]
    logging.warning("preprocessed-3[%d] <- preprocessed-2[%d] - animal rights"%(df_source_without_animal_rights.shape[0],df_source_without_duplicates.shape[0]))

    df_source_without_animal_rights.to_csv(path_preprocessed_3,sep="\t",encoding="utf-8")
    df_study = df_source_without_animal_rights[~df_source_without_animal_rights.index.isin(df_quality_checks.index)]
    logging.warning("study[%d] <- preprocessed-3[%d] - ground-truth[%d] "%(df_study.shape[0],df_source_without_animal_rights.shape[0],df_quality_checks.shape[0]))
    df_study.to_csv(path_study,sep="\t",encoding="utf-8")
    return df_study

def generate_topic_relevance_annotation_task():
    if not os.path.exists(get_path_part('topic-relevance','study')):
        df_study = generate_study_questions()

    if not os.path.exists(get_path_part('topic-relevance', 'group-1')):
        generate_groups(df_study)

    generated_batches=generate_batches()

    for batch_id in generated_batches:
        batch_label='batch-%d'%(batch_id)
        path_batch_source= get_path_part('topic-relevance', batch_label + '-source')
        path_batch=get_path_part('topic-relevance', batch_label)
        path_batch_split= get_path_part('topic-relevance', batch_label + "-split")
        path_batch_formatted=get_path_part('topic-relevance', batch_label + '-formatted')
        df_batch_source =pd.read_csv(path_batch_source,sep="\t",encoding="utf-8",index_col='question-id',dtype={'question-id':object})
        df_batch_splitted=split_batch_into_taskpages(df_batch_source,task_page_size)

        logging.warning("batch-%d-splitted[%d]"%(batch_id,df_batch_splitted.shape[0]))
        df_batch_splitted.to_csv(path_batch_split,sep="\t",encoding="utf-8")
        df_batch_with_quality_checks=generate_batch_quality_checks(batch_id,'topic-relevance')
        df_batch_with_quality_checks['task-id']=-1
        for _,df_task_page in df_batch_with_quality_checks.groupby('task-page-id'):
            df_batch_with_quality_checks.loc[df_task_page.index,'task-id']=range(1,df_task_page.shape[0]+1)


        df_topic_description = get_topic_description(df_batch_splitted)
        fill_empty_columns(df_batch_with_quality_checks)
        df_batch_with_quality_checks.reset_index(inplace=True)
        df_batch_with_examples=pd.concat([df_topic_description,df_batch_with_quality_checks])

        df_batch_with_examples.sort_values(by=['topic','task-page-id'],inplace=True)
        last_question_per_id=get_last_question_per_task_page_id(df_batch_with_examples)
        logging.warning("batch-%d-[%d] <- batch-with-quality-checks-%d[%d] + topic-descriptions[%d] "%(batch_id,df_batch_with_examples.shape[0],batch_id,df_batch_with_quality_checks.shape[0],df_topic_description.shape[0] ))
        save_batch_with_toloka_columns(df_batch_with_examples,path_batch)
        save_formmated_tasks(path_batch,path_batch_formatted,last_question_per_id)

def generate_training_dataset():
    path_training_source=get_path_part('topic-relevance', 'training-source')
    path_training=get_path_part('topic-relevance', 'training')
    df_training_source=pd.read_csv(path_training_source,sep="\t",encoding="utf-8",dtype={'topic-id':int,'task-page-id':int})
    df_training_source=df_training_source.sample(frac=1).reset_index(drop=True)
    df_training_source['task-id']=range(1,df_training_source.shape[0]+1)
    df_topic_description=get_topic_description(df_training_source)
    add_hints_for_examples(df_training_source)
    fill_empty_columns(df_training_source)
    df_training_source.sort_values(by=['topic','task-page-id'],inplace=True)
    df_training=pd.concat([df_topic_description,df_training_source])
    df_training['annotation'].loc[df_training['annotation']==-1]=0
    logging.warning("training[%d] <- training-source[%d] + topic-descriptions[%d] "%(df_training.shape[0],df_training.shape[0],df_topic_description.shape[0] ))

    save_batch_with_toloka_columns_training(df_training,path_training)





def load_topic_id_map():
    path_topic_described= get_path_described_topics('top-topics')
    df_topic_description=pd.read_csv(path_topic_described,sep="\t",encoding="utf-8")
    topics = df_topic_description['topic'].values
    topic_ids=df_topic_description['topic-id'].values
    topic_map={}
    for i,topic in enumerate(topics):
        topic_map[topic]=topic_ids[i]
    return topic_map

def add_agreed_annotations_to_quality_checks(batch):
    batch_label = "batch-%d"%batch
    logging.basicConfig(filename="../organization/quality-checks.log",level=logging.DEBUG,format='%(message)s')
    path_agreed_labels = get_path_part('topic-relevance', batch_label + "-agreed")
    group=get_group_for_batch(batch)
    path_group_quality_checks_old=get_path_part('topic-relevance', 'group-%d-quality-checks-old' % group)
    path_group_quality_checks=get_path_part('topic-relevance', 'group-%d-quality-checks' % group)

    #back up
    df_group_quality_checks_old=pd.read_csv(path_group_quality_checks,sep="\t",encoding="utf-8")
    df_group_quality_checks_old.to_csv(path_group_quality_checks_old,sep="\t",encoding="utf-8",index=False)

    df_agreed=pd.read_csv(path_agreed_labels,sep="\t",encoding="utf-8")
    df_new_batch_quality_checks=df_agreed[df_agreed['is-quality-check']==1]
    df_new_batch_quality_checks=df_new_batch_quality_checks[['INPUT:id','annotation','topic','question']]
    topic_id_map = load_topic_id_map()
    df_new_batch_quality_checks['topic-id'] =df_new_batch_quality_checks.apply(lambda row: topic_id_map[row['topic']],axis=1)
    df_new_batch_quality_checks.rename(columns={'INPUT:id':'question-id'},inplace=True)
    df_new_batch_quality_checks['batch']=batch

    df_group_quality_checks=pd.concat([df_new_batch_quality_checks,df_group_quality_checks_old])

    df_group_quality_checks.to_csv(path_group_quality_checks,encoding="utf-8",sep="\t",index=False)
    logging.warning("group-{group_id}-quality-checks[{new_size}] <- batch-{batch_id}-agreed[{agreed_size}] + group-{group_id}-quality-checks[{old_size}]".format(batch_id=batch,group_id=group,new_size=df_group_quality_checks.shape[0],old_size=df_group_quality_checks_old.shape[0],agreed_size=df_new_batch_quality_checks.shape[0]))

def does_question_need_annotations(question_row):
    count_on_topic=question_row['count.on-topic']
    count_not_on_topic=question_row['count.not-on-topic']
    count_not_a_question=question_row['count.not-a-question']
    all_accepted_annotations = count_on_topic + count_not_on_topic + count_not_a_question
    return 3 - all_accepted_annotations




def filter_questions_with_missing_annotations():
    for group in [1,2,3,4]:
        batches = group_batch_map[group]
        one_annotations_needed=[]
        two_annotations_needed=[]
        three_annotations_needed=[]
        for batch in batches:
            label_agreed="batch-%d-agreed"%batch
            label_source="batch-%d-source"%batch
            path_batch_agreed=get_path_part('topic-relevance',label_agreed)
            path_batch_source=get_path_part('topic-relevance',label_source)
            df_batch_source=pd.read_csv(path_batch_source,sep="\t",encoding="utf-8",index_col="question-id")
            df_batch_agreed=pd.read_csv(path_batch_agreed,sep="\t",encoding="utf-8")


            df_batch_agreed['annotations-needed']=df_batch_agreed.apply(does_question_need_annotations,axis=1)
            one_annotations_needed.append(df_batch_agreed[df_batch_agreed['annotations-needed']==1])
            two_annotations_needed.append(df_batch_agreed[df_batch_agreed['annotations-needed']==2])
            df_no_annotations=df_batch_source[~df_batch_source.index.isin(df_batch_agreed['INPUT:id'])]

            three_annotations_needed.append(df_no_annotations)

        df_one_annotation_batch=pd.concat(one_annotations_needed)
        df_two_annotations_batch=pd.concat(two_annotations_needed)
        df_three_annotations_batch=pd.concat(three_annotations_needed)

        rest_batches=group_batch_map_2nd_iter[group]

        df_three_annotations_batch=df_three_annotations_batch.reset_index().rename(columns={"question-id":"INPUT:id"})
        path_one_annotation_batches=get_path_part('topic-relevance-2nd','batch-%d-source'%rest_batches[0])
        path_two_annotations_batches=get_path_part('topic-relevance-2nd','batch-%d-source'%rest_batches[1])
        path_three_annotations_batches=get_path_part('topic-relevance-2nd','batch-%d-source'%rest_batches[2])

        df_one_annotation_batch[['INPUT:id','topic','question']].to_csv(path_one_annotation_batches,sep="\t",encoding="utf-8",index=False)
        df_two_annotations_batch[['INPUT:id','topic','question']].to_csv(path_two_annotations_batches,sep="\t",encoding="utf-8",index=False)
        df_three_annotations_batch[['INPUT:id','topic','question']].to_csv(path_three_annotations_batches,sep="\t",encoding="utf-8",index=False)



def generate_topic_relevance_annotation_task_iteration(dataset):
    for group in range(1,5):
        batches = group_batch_map_2nd_iter[group]
        for batch_id in batches:
            batch_label="batch-%d"%batch_id
            path_batch=get_path_part(dataset, batch_label)
            path_batch_formatted=get_path_part(dataset, batch_label + '-formatted')
            path_batch_split= get_path_part(dataset, batch_label + "-split")
            df_batch = load_batch(batch_id,dataset)
            if df_batch.shape[0]>0:
                print(batch_id)
                df_batch_splitted=split_batch_into_taskpages(df_batch,task_page_size)
                logging.warning("batch-%d-splitted[%d]"%(batch_id,df_batch_splitted.shape[0]))
                df_batch_splitted.to_csv(path_batch_split,sep="\t",encoding="utf-8",index=False)
                df_batch_with_quality_checks=generate_batch_quality_checks(batch_id,dataset)
                df_batch_with_quality_checks['task-id']=-1
                for _,df_task_page in df_batch_with_quality_checks.groupby('task-page-id'):
                    df_batch_with_quality_checks.loc[df_task_page.index,'task-id']=range(1,df_task_page.shape[0]+1)
                df_topic_description = get_topic_description(df_batch_splitted)
                fill_empty_columns(df_batch_with_quality_checks)
                df_batch_with_quality_checks.reset_index(inplace=True)
                df_batch_with_examples=pd.concat([df_topic_description,df_batch_with_quality_checks])
                df_batch_with_examples.sort_values(by=['topic','task-page-id'],inplace=True)
                last_question_per_id=get_last_question_per_task_page_id(df_batch_with_examples)
                logging.warning("batch-%d-[%d] <- batch-with-quality-checks-%d[%d] + topic-descriptions[%d] "%(batch_id,df_batch_with_examples.shape[0],batch_id,df_batch_with_quality_checks.shape[0],df_topic_description.shape[0] ))
                save_batch_with_toloka_columns(df_batch_with_examples,path_batch)
                save_formmated_tasks(path_batch,path_batch_formatted,last_question_per_id)

def produce_dataset(study):
    #for group in group_batch_map:
    all_gorups=[]
    for group in [1,2,3,4]:
        path_group_final=get_path_part(study,'group-%d-production'%group)
        all_batches=[]
        for batch in group_batch_map[group]:
            path_agreed_2nd_iter= get_path_part(study,'batch-%d-agreed-2nd'%batch)
            df_batch_results=pd.read_csv(path_agreed_2nd_iter,sep="\t",encoding="utf-8")
            all_batches.append(df_batch_results)

        print(batch)
        path_agreed_2nd_iter= get_path_part('topic-relevance-2nd','batch-%d-agreed-2nd'%group_batch_map_2nd_iter[group][-1])
        if path_agreed_2nd_iter!=None and os.path.exists(path_agreed_2nd_iter):
            df_batch_results=pd.read_csv(path_agreed_2nd_iter,sep="\t",encoding="utf-8")
            all_batches.append(df_batch_results)
        df_group=pd.concat(all_batches)
        df_group.to_csv(path_group_final,sep="\t",encoding="utf-8",index=False)
        all_gorups.append(df_group)
    path_production=get_path_part(study,'production')
    df_production=pd.concat(all_gorups)
    df_production.to_csv(path_production,sep="\t",encoding="utf-8")
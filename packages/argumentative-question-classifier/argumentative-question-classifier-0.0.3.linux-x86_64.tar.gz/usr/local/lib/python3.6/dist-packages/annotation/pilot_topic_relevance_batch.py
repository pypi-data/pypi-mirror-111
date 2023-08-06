import pandas as pd
from conf.configuration import *
from annotation.topics import *
import random
import sys
import  logging
file_path= os.path.dirname(__file__)

def load_examples_df_for_batch(batch):

    label='batch-%d-examples-extended'%batch
    path_batch_examples= get_path_part('pilot-topic-relevance', label)
    df_batch1_examples = pd.read_csv(path_batch_examples,sep="\t",encoding="utf-8")
    return df_batch1_examples

def load_guidelines():

    path = "/home/yamenajjour/IdeaProjects/subjective-questions-taxonomy/organization/guidelines-topic-relevance-ru-parameterized.txt"
    with open(path,'r') as content_file:
        guideline = "".join(content_file.readlines())
    return guideline

def generate_batch_1_quality_checks( count_on_topic_checks_batch, count_not_on_topic_checks_batch, count_not_a_question_check_batch):
    path_quality_checks= get_path_part('pilot-topic-relevance', 'quality-checks')
    df_quality_checks= pd.read_csv(path_quality_checks,sep="\t",encoding="utf-8")
    path_batch1_quality_checks= get_path_part('pilot-topic-relevance', 'batch-1-quality-checks')


    dfs_on_topic_quality_checks=[]
    # getting on topic quality checks
    for topic, quality_checks_per_topic in list(df_quality_checks.groupby('topic')):
        on_topic_quality_checks = quality_checks_per_topic[quality_checks_per_topic.annotation==0]
        on_topic_quality_checks_sample=on_topic_quality_checks.sample(n=count_on_topic_checks_batch)
        dfs_on_topic_quality_checks.append(on_topic_quality_checks_sample)
    df_on_topic_quality_checks=pd.concat(dfs_on_topic_quality_checks)
    dfs_not_on_topic_quality_checks=[]
    # drop on topic quality checks to prevent a question from being included twice as on topic for one and not on topic for one
    df_quality_checks=df_quality_checks.drop(df_on_topic_quality_checks.index)
    # generate not on topic quality checks
    for topic, quality_checks_per_topic in list(df_quality_checks.groupby('topic')):
        not_on_topic_quality_checks = quality_checks_per_topic.loc[quality_checks_per_topic.annotation==1]
        count_not_on_topic_quality_checks= not_on_topic_quality_checks.shape[0]
        if count_not_on_topic_quality_checks >= count_not_a_question_check_batch:
            sample_not_on_topic_quality_chekcs=not_on_topic_quality_checks.sample(n=count_not_a_question_check_batch)
            dfs_not_on_topic_quality_checks.append(sample_not_on_topic_quality_chekcs)
        else:
            count_quality_checks_to_sample = count_not_on_topic_checks_batch - count_not_on_topic_quality_checks
            if count_not_on_topic_quality_checks >0:
                dfs_not_on_topic_quality_checks.append(not_on_topic_quality_checks)
            quality_checks_other_topics=df_quality_checks[df_quality_checks.topic!=topic]

            df_not_on_topic_questions=quality_checks_other_topics.loc[quality_checks_other_topics.annotation==0].sample(n=count_quality_checks_to_sample)
            df_not_on_topic_questions.loc[:,'topic']=topic
            df_not_on_topic_questions.loc[:,'annotation']=1
            dfs_not_on_topic_quality_checks.append(df_not_on_topic_questions)
    df_not_on_topic_quality_checks=pd.concat(dfs_not_on_topic_quality_checks)
    # generate not a question quality checks
    dfs_not_a_question_quality_checks = []
    for topic, quality_checks_per_topic in list(df_quality_checks.groupby('topic')):
        not_a_question_quality_checks = quality_checks_per_topic.loc[quality_checks_per_topic.annotation==2]
        count_not_a_question_quality_checks = not_a_question_quality_checks.shape[0]
        if count_not_a_question_quality_checks ==0:
            continue
        if count_not_a_question_check_batch > count_not_a_question_quality_checks:
            dfs_not_a_question_quality_checks.append(not_a_question_quality_checks)
        else:
            dfs_not_a_question_quality_checks.append(not_a_question_quality_checks.sample(count_not_a_question_check_batch))

    df_not_a_question_quality_checks = pd.concat(dfs_not_a_question_quality_checks)

    df_batch1_quality_checks= pd.concat([df_on_topic_quality_checks,df_not_on_topic_quality_checks, df_not_a_question_quality_checks])
    #generate_statistics(df_batch1_quality_checks)
    df_batch1_quality_checks.to_csv(path_batch1_quality_checks,sep='\t', encoding='utf-8', index=False)


def generate_batch_i_quality_checks(batch, count_on_topic_checks_batch, count_not_on_topic_checks_batch, count_not_a_question_check_batch):

    if batch == 1:
        path_quality_checks= get_path_part('pilot-topic-relevance', 'quality-checks')
        df_quality_checks= pd.read_csv(path_quality_checks,sep="\t",encoding="utf-8")
    else:
        quality_check_batch = batch -1
        quality_checks_label='batch-%d-agreed'%quality_check_batch
        path_quality_checks= get_path_part('pilot-topic-relevance', quality_checks_label)
        df_quality_checks= pd.read_csv(path_quality_checks,sep="\t",encoding="utf-8")
        df_quality_checks.rename(columns={'INPUT:id':'question-id'},inplace=True)
    batch_i_quality_checks_label='batch-%d-quality-checks'%batch
    path_batch_i_quality_checks= get_path_part('pilot-topic-relevance', batch_i_quality_checks_label)


    dfs_on_topic_quality_checks=[]
    # getting on topic quality checks
    for topic, quality_checks_per_topic in list(df_quality_checks.groupby('topic')):
        on_topic_quality_checks = quality_checks_per_topic[quality_checks_per_topic.annotation==0]
        on_topic_quality_checks_sample=on_topic_quality_checks.sample(n=count_on_topic_checks_batch)
        dfs_on_topic_quality_checks.append(on_topic_quality_checks_sample)
    df_on_topic_quality_checks=pd.concat(dfs_on_topic_quality_checks)
    dfs_not_on_topic_quality_checks=[]
    # drop on topic quality checks to prevent a question from being included twice as on topic for one and not on topic for one
    df_quality_checks=df_quality_checks.drop(df_on_topic_quality_checks.index)
    # generate not on topic quality checks
    for topic, quality_checks_per_topic in list(df_quality_checks.groupby('topic')):
        not_on_topic_quality_checks = quality_checks_per_topic.loc[quality_checks_per_topic.annotation==1]
        count_not_on_topic_quality_checks= not_on_topic_quality_checks.shape[0]
        if count_not_on_topic_quality_checks >= count_not_a_question_check_batch:
            sample_not_on_topic_quality_chekcs=not_on_topic_quality_checks.sample(n=count_not_a_question_check_batch)
            dfs_not_on_topic_quality_checks.append(sample_not_on_topic_quality_chekcs)
        else:
            count_quality_checks_to_sample = count_not_on_topic_checks_batch - count_not_on_topic_quality_checks
            if count_not_on_topic_quality_checks >0:
                dfs_not_on_topic_quality_checks.append(not_on_topic_quality_checks)
            quality_checks_other_topics=df_quality_checks[df_quality_checks.topic!=topic]

            df_not_on_topic_questions=quality_checks_other_topics.loc[quality_checks_other_topics.annotation==0].sample(n=count_quality_checks_to_sample)
            df_not_on_topic_questions.loc[:,'topic']=topic
            df_not_on_topic_questions.loc[:,'annotation']=1
            dfs_not_on_topic_quality_checks.append(df_not_on_topic_questions)
    df_not_on_topic_quality_checks=pd.concat(dfs_not_on_topic_quality_checks)
    # generate not a question quality checks
    dfs_not_a_question_quality_checks = []
    for topic, quality_checks_per_topic in list(df_quality_checks.groupby('topic')):
        not_a_question_quality_checks = quality_checks_per_topic.loc[quality_checks_per_topic.annotation==2]
        count_not_a_question_quality_checks = not_a_question_quality_checks.shape[0]
        if count_not_a_question_quality_checks ==0:
            continue
        if count_not_a_question_check_batch > count_not_a_question_quality_checks:
            dfs_not_a_question_quality_checks.append(not_a_question_quality_checks)
        else:
            dfs_not_a_question_quality_checks.append(not_a_question_quality_checks.sample(count_not_a_question_check_batch))

    df_not_a_question_quality_checks = pd.concat(dfs_not_a_question_quality_checks)

    df_batch_quality_checks= pd.concat([df_on_topic_quality_checks,df_not_on_topic_quality_checks, df_not_a_question_quality_checks])
    #generate_statistics(df_batch1_quality_checks)
    df_batch_quality_checks.to_csv(path_batch_i_quality_checks,sep='\t', encoding='utf-8', index=False)


def load_topic_description_tasks(batch):
    df_topic_description=load_topic_description_df()
    df_topic_description=df_topic_description[['Russian-description','topic']]
    df_topic_description['question-id']=[-1 *x for x in range(len(df_topic_description.index))]
    df_topic_description['question']=["question" for index in df_topic_description.index]
    df_topic_description['annotation']=[-1 for index in df_topic_description.index]
    df_topic_description['on-topic-example']=""
    df_topic_description['not-on-topic-example']=""
    df_topic_description['not-a-question-example']=""

    df_examples =load_examples_df_for_batch(batch)
    for index, row in df_topic_description.iterrows():
        topic = row['topic']
        logging.warning('retrieving examples for topic %s',topic)
        on_topic_question_example=df_examples.loc[(df_examples['topic']==topic) & (df_examples['annotation'] ==0),'question'].values[0]
        not_on_topic_question_example=df_examples.loc[(df_examples['topic']==topic) & (df_examples['annotation'] ==1),'question'].values[0]
        not_a_question_example=df_examples.loc[(df_examples['topic']==topic) & (df_examples['annotation'] ==2),'question'].values[0]

        logging.warning('On topic question for %s is %s'%(topic,on_topic_question_example))
        logging.warning('Not on topic question for %s is %s'%(topic,not_on_topic_question_example))
        logging.warning('Not a question for %s is %s'%(topic,not_a_question_example))



        df_topic_description.loc[index,'on-topic-example']=on_topic_question_example
        df_topic_description.loc[index,'not-on-topic-example']=not_on_topic_question_example
        df_topic_description.loc[index,'not-a-question-example']=not_a_question_example

        logging.warning(df_topic_description.loc[index,'Russian-description'])


    return df_topic_description

def save_formmated_tasks(path_batch_final,path_batch_formatted,last_question_id_per_topic):
    skip_header=False
    with open(path_batch_final,'r') as file_annotation_tasks:
        with open(path_batch_formatted,'w') as file_annotation_tasks_batches:
            for line in file_annotation_tasks:
                if not skip_header:
                    file_annotation_tasks_batches.write(line)
                    skip_header=True
                    continue
                question_id = line.split('\t')[0]
                if int(question_id) in list(last_question_id_per_topic):
                    file_annotation_tasks_batches.write(line+"\n")
                else:

                    file_annotation_tasks_batches.write(line)
def fill_empty_columns(dataframe):
    dataframe['Russian-description']="description"
    dataframe['on-topic-example']="on-topic-example"
    dataframe['not-on-topic-example']="not-on-topic-example"
    dataframe['not-a-question-example']="not-a-question-example"

def prepare_batch_toloka(batch):
    batch_label="batch-%d"%batch
    path_batch_quality_checks= get_path_part('pilot-topic-relevance', batch_label + '-quality-checks')
    df_batch_quality_checks=pd.read_csv(path_batch_quality_checks,sep="\t",encoding="utf-8",dtype={'question-id':int})

    path_batch_batch_source= get_path_part('pilot-topic-relevance', batch_label + '-source')
    path_batch_batch_with_descriptions= get_path_part('pilot-topic-relevance', batch_label + '-with-descriptions')
    df_batch = pd.read_csv(path_batch_batch_source,sep="\t",encoding="utf-8",dtype={'question-id':int})

    del df_batch['phrase-id']

    df_batch['Russian-description']="description"
    fill_empty_columns(df_batch)
    fill_empty_columns(df_batch_quality_checks)

    df_topic_descriptions = load_topic_description_tasks(batch)
    df_batch_with_quality_checks = pd.concat([df_batch_quality_checks,df_batch ,df_topic_descriptions])
    df_batch_with_quality_checks=df_batch_with_quality_checks.sample(frac=1).reset_index(drop=True)
    print(df_batch_quality_checks.info())
    df_batch_with_quality_checks['temp-index']=df_batch_with_quality_checks.apply(lambda row: row['question-id']>0,axis=1)
    df_batch_with_quality_checks.sort_values(['topic','temp-index'],inplace=True)
    print(df_batch_quality_checks[['topic','question']])
    last_topic=df_batch_with_quality_checks.iloc[0,df_batch_with_quality_checks.columns.get_loc('topic')]
    last_question_id_per_topic=[]
    last_index=None
    for index,row in df_batch_with_quality_checks.iterrows():
        if row['topic']!=last_topic:
            last_question_id=df_batch_with_quality_checks.loc[last_index,'question-id']
            last_topic=row['topic']
            last_question_id_per_topic.append(last_question_id)
        last_index=index

    #last_question_id_per_topic = df_batch_with_quality_checks.copy().groupby('topic')['question-id'].max()

    df_batch_toloka_format = df_batch_with_quality_checks[['question','question-id','Russian-description','annotation','on-topic-example','not-on-topic-example','not-a-question-example']].rename(
        columns={'question-id':"INPUT:id","question":"INPUT:question","Russian-description":"INPUT:topic-description","annotation":"GOLDEN:category"
                 ,"on-topic-example":"INPUT:on-topic-example","not-on-topic-example":"INPUT:not-on-topic-example","not-a-question-example":"INPUT:not-a-question-example"
                 })
    df_batch_toloka_format['GOLDEN:category']=df_batch_toloka_format['GOLDEN:category'].fillna(-1).astype(int)
    df_batch_toloka_format['GOLDEN:category'].loc[df_batch_toloka_format['GOLDEN:category']==-1]=""
    path_batch_final = get_path_part('pilot-topic-relevance', batch_label)
    logging.warning(df_batch_toloka_format.info())
    df_batch_toloka_format.to_csv(path_batch_final ,sep="\t",encoding="utf-8",columns=['INPUT:id','INPUT:question','INPUT:topic-description',
                                                                                         'INPUT:on-topic-example','INPUT:not-on-topic-example','INPUT:not-a-question-example','GOLDEN:category'],index=False)
    df_batch_with_quality_checks.to_csv(path_batch_batch_with_descriptions,sep="\t",encoding="utf-8")
    path_batch_formatted = get_path_part('pilot-topic-relevance', batch_label + '-formatted')
    save_formmated_tasks(path_batch_final,path_batch_formatted,last_question_id_per_topic )

def generate_training_dataset_for_batch(batch):
    path_training= get_path_part('pilot-topic-relevance', 'training')
    df_training=pd.read_csv(path_training,sep="\t",encoding="utf-8")
    df_topic_descriptions=load_topic_description_tasks(batch)
    df_topic_descriptions = df_topic_descriptions[df_topic_descriptions['topic']=='ЮКОС']
    df_topic_descriptions['hint']="HINT"
    fill_empty_columns(df_training)
    df_training_with_topic_descriptions=pd.concat([df_topic_descriptions,df_training])
    logging.warning(df_training.info())
    logging.warning(df_topic_descriptions.info())
    df_training_with_topic_descriptions=df_training_with_topic_descriptions.sort_values(['topic','question-id'])
    last_question_id_per_topic = df_training_with_topic_descriptions.copy().groupby('topic')['question-id'].max()
    path_training_batch_1= get_path_part('pilot-topic-relevance', 'training-batch-%d' % batch)
    print(df_training_with_topic_descriptions.info())
    df_training_with_topic_descriptions=df_training_with_topic_descriptions[['question','question-id','Russian-description','annotation','on-topic-example','hint','not-on-topic-example','not-a-question-example']]
    df_training_with_topic_descriptions.rename(
        columns={'question-id':"INPUT:id","question":"INPUT:question","Russian-description":"INPUT:topic-description","annotation":"GOLDEN:category"
            ,"on-topic-example":"INPUT:on-topic-example","not-on-topic-example":"INPUT:not-on-topic-example","not-a-question-example":"INPUT:not-a-question-example","hint":"HINT:text"
                 },inplace=True)
    df_training_with_topic_descriptions['GOLDEN:category'].loc[df_training_with_topic_descriptions['GOLDEN:category']==-1]=0
    df_training_with_topic_descriptions.to_csv(path_training_batch_1,sep="\t",encoding="utf-8",columns=['INPUT:id','INPUT:question','INPUT:topic-description',
                                                                                                        'INPUT:on-topic-example','INPUT:not-on-topic-example','HINT:text','INPUT:not-a-question-example','GOLDEN:category'],index=False)
    path_training_batch_1_formatted= get_path_part('pilot-topic-relevance', 'training-batch-%d-formatted' % batch)
    save_formmated_tasks(path_training_batch_1,path_training_batch_1_formatted,last_question_id_per_topic)

def generate_examples_for_batch(batch):
    path_non_training_non_ground_truth=get_path_part('pilot-topic-relevance', 'ground-truth-non-training-non-quality-checks')
    path_examples=get_path_part('pilot-topic-relevance', 'examples')
    df_examples=pd.read_csv(path_examples,sep="\t",encoding="utf-8")
    label='batch-%d-examples'%batch
    path_batch_examples= get_path_part('pilot-topic-relevance', label)
    df_non_training_non_ground_truth = pd.read_csv(path_non_training_non_ground_truth,sep="\t",encoding="utf-8")
    if batch!=4:
        examples_batch=batch+1
    if batch ==4:
        examples_batch=1
    examples_batch = 'batch-%d-source'%examples_batch
    path_examples_batch= get_path_part('pilot-topic-relevance', examples_batch)
    df_examples_batch=pd.read_csv(path_examples_batch,sep="\t",encoding="utf-8")
    df_examples_batch=df_examples_batch[['question-id']]
    print(df_examples_batch.shape[0])
    df_examples_batch_with_annotations=df_non_training_non_ground_truth.merge(df_examples_batch,on="question-id")
    df_examples_batch_with_annotations = pd.concat([df_examples_batch_with_annotations, df_examples])
    print(df_examples_batch_with_annotations.shape[0])
    all_questions=[]

    for topic, questions_per_topic in df_examples_batch_with_annotations.groupby('topic'):
        df_on_topic_questions=questions_per_topic[questions_per_topic['annotation']==0]
        df_not_on_topic_questions=questions_per_topic[questions_per_topic['annotation']==1]
        df_not_questions=questions_per_topic[questions_per_topic['annotation']==2]
        if df_on_topic_questions.shape[0]>0:
            on_topic_question=df_on_topic_questions.sample(n=1)
            all_questions.append(on_topic_question)
        if df_not_on_topic_questions.shape[0]>0:
            not_on_topic_question=df_not_on_topic_questions.sample(n=1)
            all_questions.append(not_on_topic_question)
        if df_not_questions.shape[0]>0:
            not_a_question=df_not_questions.sample(n=1)
            all_questions.append(not_a_question)


    df_example_questions=pd.concat(all_questions)
    df_example_questions.to_csv(path_batch_examples,sep="\t",encoding="utf-8",index=False)



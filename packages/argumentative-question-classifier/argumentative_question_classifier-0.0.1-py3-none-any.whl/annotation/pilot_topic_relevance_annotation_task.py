import pandas as pd
from conf.configuration import *
import math
from collections import Counter
from annotation.topics import *
from annotation.pilot_topic_relevance_batch import *

training_sample_size_per_topic=25
quality_check_percentage = 0.25
count_of_questions_per_page=15
count_of_quality_checks_per_page=3




def get_hints():
    hints = {}
    hints[0]= 'вопрос относится к данной теме'
    hints[1]= 'не по теме: вопрос не связан с данной темой.'
    hints[2]= 'не вопрос: представленный текст не является вопросом.'
    return hints


def generate_statistics(dataframe):
    print(dataframe['topic'].value_counts().to_string())
    print(dataframe.groupby('topic').agg({'annotation':lambda x: str(Counter(sorted(x)))}))

def merge_on_topic_labels():
    def merge_labels(row):
        if row['annotation'] in [0,1,2,5,6]:
            return 0
        elif row['annotation'] == 4:
            return 1
        elif row['annotation']==3:
            return 2
        elif row['annotation']==-1:
            return -1
        else:
            raise ValueError("Unknown value")

    path_agreed_questions= get_pilotstudy_dataset_agreed_path('pilot-study-top-topics-sample-corrected')
    df_agreed_questions=pd.read_csv(path_agreed_questions,sep="\t",encoding="utf-8",index_col='question-id')
    df_agreed_questions['new-annotation']=df_agreed_questions.apply(merge_labels,axis=1)
    df_agreed_questions=df_agreed_questions[df_agreed_questions['new-annotation']!=-1]
    del df_agreed_questions['annotation']
    df_agreed_questions.rename(columns={'new-annotation':'annotation'},inplace=True)
    path_ground_truth= get_path_part('pilot-topic-relevance', 'ground-truth')
    df_agreed_questions.to_csv(path_ground_truth,sep="\t",encoding="utf-8")

def generate_training_dataset(df_ground_truth,training_sample_size_per_topic):

    training_topics=['ЮКОС']
    training_datasets=[]
    for topic in training_topics:
        df_topic_questions=df_ground_truth[df_ground_truth['topic']==topic]
        df_training_instances=df_topic_questions.sample(n=training_sample_size_per_topic)
        training_datasets.append(df_training_instances)

    df_training_dataset = pd.concat(training_datasets)
    df_training_dataset_copy=df_training_dataset.copy()

    random_index= list(range(0,len(df_training_dataset.index)))
    df_training_dataset=df_training_dataset.reset_index()
    df_training_dataset['index']=random_index
    df_training_dataset=df_training_dataset.set_index('index')


    hints = get_hints()
    df_training_dataset['hint']=df_training_dataset.apply(lambda question: hints[int(question['annotation'])],axis=1)

    return df_training_dataset,df_training_dataset_copy

def generate_quality_checks(df_non_training_ground_truth,quality_check_percentage):
    quality_check_list=[]
    non_training_ground_truth = list(df_non_training_ground_truth.groupby('topic'))
    for topic, questions_per_topic in non_training_ground_truth:
        df_topic_quality_checks=questions_per_topic.sample(frac=quality_check_percentage)
        quality_check_list.append(df_topic_quality_checks)
    df_quality_checks=pd.concat(quality_check_list)
    return df_quality_checks

def generate_topic_quality_checks_pools(df_topic_quality_checks):
    df_topic_quality_checks_not_on_topic=df_topic_quality_checks[df_topic_quality_checks['annotation'] == 1]
    df_topic_quality_checks_on_topic=df_topic_quality_checks[df_topic_quality_checks['annotation'] == 0]
    df_topic_quality_checks_not_questions=df_topic_quality_checks[df_topic_quality_checks['annotation'] == 2]
    return df_topic_quality_checks_on_topic,df_topic_quality_checks_not_on_topic,df_topic_quality_checks_not_questions

def sample_page_quality_checks(df_topic_quality_checks,count):
        return df_topic_quality_checks.sample(n=count)


def generate_batches(df_study_questions):
    batch1_questions=[]
    batch2_questions=[]
    batch3_questions=[]
    batch4_questions=[]

    study_questions_per_topic = list(df_study_questions.groupby('topic'))
    for topic, df_topic_questions in study_questions_per_topic:
        df_topic_questions_batch1 = df_topic_questions.sample(frac=1/4.0)
        batch1_questions.append(df_topic_questions_batch1)

        df_topic_questions=df_topic_questions.drop(df_topic_questions_batch1.index)
        df_topic_questions_batch2 = df_topic_questions.sample(n=df_topic_questions_batch1.shape[0])
        batch2_questions.append(df_topic_questions_batch2)

        df_topic_questions = df_topic_questions.drop(df_topic_questions_batch2.index)
        df_topic_questions_batch3 = df_topic_questions.sample(n=df_topic_questions_batch1.shape[0])
        batch3_questions.append(df_topic_questions_batch3)
        df_topic_questions_batch4 = df_topic_questions.drop(df_topic_questions_batch3.index)
        batch4_questions.append(df_topic_questions_batch4)

    df_batch_1=pd.concat(batch1_questions)
    df_batch_2=pd.concat(batch2_questions)
    df_batch_3=pd.concat(batch3_questions)
    df_batch_4=pd.concat(batch4_questions)

    path_batch_1_source= get_path_part('pilot-topic-relevance', 'batch-1-source')
    path_batch_2_source= get_path_part('pilot-topic-relevance', 'batch-2-source')
    path_batch_3_source= get_path_part('pilot-topic-relevance', 'batch-3-source')
    path_batch_4_source= get_path_part('pilot-topic-relevance', 'batch-4-source')


    df_batch_1.to_csv(path_batch_1_source,sep="\t",encoding='utf-8')
    df_batch_2.to_csv(path_batch_2_source,sep="\t",encoding='utf-8')
    df_batch_3.to_csv(path_batch_3_source,sep="\t",encoding='utf-8')
    df_batch_4.to_csv(path_batch_4_source,sep="\t",encoding='utf-8')

def generate_topic_relevance_annotation_task():

    path_topic_relevance_source= get_source_path('pilot-topic-relevance')
    df_questions = pd.read_csv(path_topic_relevance_source,sep="\t",encoding="utf-8",index_col='question-id')
    path_ground_truth= get_path_part('pilot-topic-relevance', 'ground-truth')
    df_ground_truth = pd.read_csv(path_ground_truth,sep="\t",encoding="utf-8",index_col='question-id')

    path_non_training_ground_truth=get_path_part('pilot-topic-relevance', 'ground-truth-non-training')
    path_non_training_source=get_path_part('pilot-topic-relevance', 'source-non-training')
    path_non_training_non_quality_checks_source=get_path_part('pilot-topic-relevance', 'source-non-training-non-quality-checks')
    # generate training dataset

    df_training, df_training_dataset=generate_training_dataset(df_ground_truth,training_sample_size_per_topic)

    path_training= get_path_part('pilot-topic-relevance', 'training')
    print(path_training)
    print(df_training.info())
    df_training.to_csv(path_training,sep='\t', encoding='utf-8',index=False)


    df_questions_only=df_questions[['question']]
    df_non_training_ground_truth=df_ground_truth[~df_ground_truth.isin(df_training_dataset).all(1)]
    df_non_training_ground_truth.to_csv(path_non_training_ground_truth,sep="\t",encoding="utf-8")
    #generating quality checks

    df_quality_checks = generate_quality_checks(df_non_training_ground_truth,quality_check_percentage)
    path_quality_checks= get_path_part('pilot-topic-relevance', 'quality-checks')
    df_quality_checks.to_csv(path_quality_checks,sep='\t', encoding='utf-8')



    df_study_questions=df_questions[~df_questions_only.isin(df_training_dataset['question']).all(1)]
    df_study_questions.to_csv(path_non_training_source,sep="\t",encoding="utf-8")
    df_questions_only=df_study_questions[['question']]
    df_study_questions=df_study_questions[~df_questions_only.isin(df_quality_checks['question']).all(1)]
    df_study_questions.to_csv(path_non_training_non_quality_checks_source,sep="\t",encoding="utf-8")
    generate_batches(df_study_questions)


def update_topic_describtion():
    path_training= get_path_part('pilot-topic-relevance', 'training')
    df_training_dataset= pd.read_csv(path_training,sep="\t",encoding="utf-8")
    path_ground_truth= get_path_part('pilot-topic-relevance', 'ground-truth')
    df_ground_truth = pd.read_csv(path_ground_truth,sep="\t",encoding="utf-8")
    df_ground_truth = df_ground_truth[['question-id','topic']]
    df_training_dataset.rename(columns={"INPUT:id":'question-id'},inplace=True)
    df_training_dataset = pd.merge(df_training_dataset,df_ground_truth,how='left',on='question-id')
    df_topic_descriptions= load_topic_description_df()
    for index,row in df_training_dataset.iterrows():
        topic = row['topic']
        topic_description= df_topic_descriptions.loc[df_topic_descriptions['topic']==topic,'Russian-description'].iloc[0]
        df_training_dataset.loc[index,'INPUT:topic-description']=topic_description
    df_training_dataset.rename(columns={'question-id':"INPUT:id"},inplace=True)
    del df_training_dataset['topic']
    df_training_dataset.to_csv(path_training+".2",sep="\t",encoding="utf-8",index=False)


def generate_ground_truth_non_training_non_qulaity_checks():
    # those questions were generated to extract examples for the annotation quidelines
    path_non_training_non_ground_truth=get_path_part('pilot-topic-relevance', 'ground-truth-non-training-non-quality-checks')
    path_non_training_ground_truth=get_path_part('pilot-topic-relevance', 'ground-truth-non-training')

    path_quality_checks = get_path_part('pilot-topic-relevance', 'quality-checks')
    df_non_training_ground_truth = pd.read_csv(path_non_training_ground_truth,sep="\t",encoding="utf-8")
    print(path_quality_checks)
    df_quality_checks = pd.read_csv(path_quality_checks,sep="\t",encoding="utf-8")
    print(df_non_training_ground_truth.shape[0])
    df_non_training_ground_truth_ids=df_non_training_ground_truth['question']
    df_non_training_non_ground_truth=df_non_training_ground_truth[~df_non_training_ground_truth_ids.isin(df_quality_checks['question'])]
    print(df_quality_checks.shape[0])
    df_non_training_non_ground_truth.to_csv(path_non_training_non_ground_truth,sep="\t",encoding="utf-8",index=False)

    print(df_non_training_non_ground_truth.shape[0])


#generate_ground_truth_non_training_non_qulaity_checks()

#    df_training_dataset.to_csv(trianing_path,sep="\t",encoding="utf-8")
 #   print(trianing_path)
    #get quality checks

    #add topic description

    #generate header file

#merge_on_topic_labels()
#update_topic_describtion()
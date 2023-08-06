from conf.configuration import *
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from random import randint
def drop_no_agreement(df_source):
    return df_source[df_source['annotation']!=-1]

def convert_nota_question(df_source):
    df_source['annotation']=df_source['annotation'].apply(lambda annotation: 1 if annotation == 2 else annotation)
    return df_source

def load_topics():
    path_topic_described= get_path_described_topics('top-topics')
    df_topic_description=pd.read_csv(path_topic_described,sep="\t",encoding="utf-8")
    df_topic_description=df_topic_description[['topic','topic-id']]
    return df_topic_description

def clean_source(df_source):
    df_source.rename(columns={'INPUT:id':'question-id'},inplace=True)
    df_source=df_source[['question','topic','annotation']]
    df_topics=load_topics()
    df_source=df_source.merge(df_topics,on='topic')
    df_source = drop_no_agreement(df_source)
    df_source = convert_nota_question(df_source)
    return df_source

def setup_in_topic_experiment(experiment_in_topic, num_splits):
    path_source = get_source_path(experiment_in_topic)

    split = StratifiedShuffleSplit(n_splits=num_splits, test_size=0.2, random_state=randint(0, 100))
    df_source = pd.read_csv(path_source, sep="\t", encoding="utf-8", index_col='INPUT:id')
    df_source=clean_source(df_source)


    counter = 0
    df_source.index = df_source.index.to_numpy()
    for train_index, test_index in split.split(df_source, df_source['topic-id']):
        df_training_set = df_source.iloc[train_index]
        df_test_set = df_source.iloc[test_index]

        path_training = get_path_experiment_part(experiment_in_topic, counter, 'train')
        path_test = get_path_experiment_part(experiment_in_topic, counter, 'test')

        df_training_set.to_csv(path_training, sep="\t", encoding="utf-8", index=False)
        df_test_set.to_csv(path_test, sep="\t", encoding="utf-8", index=False)
        counter = counter + 1


def setup_cross_topic_experiment(experiment_cross_topic, topic_ids):
    path_source = get_source_path(experiment_cross_topic)

    df_source = pd.read_csv(path_source, sep="\t", encoding="utf-8", index_col='INPUT:id')
    df_source=clean_source(df_source)



    for topic_id in topic_ids:
        df_topic_questions_test = df_source[df_source['topic-id'] == topic_id]
        df_topic_questions_train = df_source[df_source['topic-id'] != topic_id]

        path_test = get_path_experiment_part(experiment_cross_topic, topic_id, 'test')
        path_train = get_path_experiment_part(experiment_cross_topic, topic_id, 'train')

        df_topic_questions_train.to_csv(path_train, sep="\t", encoding="utf-8", index=False)
        df_topic_questions_test.to_csv(path_test, sep="\t", encoding="utf-8", index=False)

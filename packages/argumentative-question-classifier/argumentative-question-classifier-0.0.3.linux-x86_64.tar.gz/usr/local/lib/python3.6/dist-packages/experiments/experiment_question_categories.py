import pandas as pd
from conf.configuration import *
from sklearn.model_selection import StratifiedShuffleSplit
from random import randint



def convert_dont_know(df_dataset, label):
    df_dataset['annotation'] = df_dataset['annotation'].replace(-1, label)


def drop_dont_know(df_dataset):
    return df_dataset[df_dataset['annotation'] != -1]


def show_label_distribution(experiment):
    path_source = get_source_path(experiment)
    df_source = pd.read_csv(path_source, sep="\t", encoding="utf-8")
    return df_source['annotation'].value_counts().to_dict()


def setup_cross_topic_experiment(experiment_cross_topic, topic_ids):
    path_source = get_source_path(experiment_cross_topic)
    df_source = pd.read_csv(path_source, sep="\t", encoding="utf-8")
    df_source = drop_dont_know(df_source)
    for topic_id in topic_ids:
        df_topic_questions_test = df_source[df_source['topic-id'] == topic_id]
        df_topic_questions_train = df_source[df_source['topic-id'] != topic_id]

        path_test = get_path_experiment_part(experiment_cross_topic, topic_id, 'test')
        path_train = get_path_experiment_part(experiment_cross_topic, topic_id, 'train')

        df_topic_questions_train.to_csv(path_train, sep="\t", encoding="utf-8", index=False)
        df_topic_questions_test.to_csv(path_test, sep="\t", encoding="utf-8", index=False)


def setup_in_topic_experiment(experiment_in_topic, num_splits):
    path_source = get_source_path(experiment_in_topic)
    split = StratifiedShuffleSplit(n_splits=num_splits, test_size=0.2, random_state=randint(0, 100))
    df_source = pd.read_csv(path_source, sep="\t", encoding="utf-8", index_col='question-id')
    df_source = drop_dont_know(df_source)
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



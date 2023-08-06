import pandas as pd
from conf.configuration import *
from preprocessing.mturk_preprocess import *
import matplotlib.pyplot as plt
import time,csv

def load_controversial_topics():
    topics= []
    wikipedia_controversial_topics_path = get_wikipedia_controversial_topics_path()
    wikipedia_controversial_topics_file = open(wikipedia_controversial_topics_path,'r')
    for line in wikipedia_controversial_topics_file:
        topics.append(line.lower().strip())
    return topics




def load_controversial_topics_translted():
    topics = []
    controversial_topics_translated_path = get_wikipedia_controversial_topics_path('translated')
    translated_topics_df = pd.read_csv(controversial_topics_translated_path,sep=',',encoding='utf-8')
    translated_topics_list = list(translated_topics_df['translated_topic'])
    for topic in translated_topics_list:
        topics.append(topic.lower())
    return topics

def write_yandex_controversial_topic_statistics():
    translated_controversial_topics = load_controversial_topics_translted()
    yandex_controversial_questions = get_sampled_controversial_path('yandex',2)
    controversy_questions_df = pd.read_csv(yandex_controversial_questions,sep=',', encoding='utf-8')
    controversial_topic_counts = []

    for topic in translated_controversial_topics:
        topic_df = controversy_questions_df[controversy_questions_df['question'].str.contains(topic)]
        count= len(topic_df)
        controversial_topic_counts.append(count)

    bins = range(0,10000,100)
    fig, ax = plt.subplots()
    hist = ax.hist(controversial_topic_counts, bins, histtype='bar', rwidth=0.8)
    print(len(hist[0]),len(hist[1]))
    frequencies = hist[0].tolist()
    frequencies.append(-111)
    topic_counts = hist[1].tolist()
    histogram_df = pd.DataFrame({'topic-counts':topic_counts,'frequencies':frequencies})
    histogram_path= get_histogram_path("yandex","topics")
    histogram_figure_path= get_histogram_path_figure("yandex","topics")
    histogram_df.to_csv(histogram_path,sep=',',encoding='utf-8')
    print(histogram_figure_path)
    fig.savefig(histogram_figure_path)

def write_yahoo_controversial_topics_statistics():
    controversial_topics= load_controversial_topics()

    yahoo_controversial_sampled_1 = get_sampled_controversial_path("yahoo",1)
    controversy_questions_df = pd.read_csv(yahoo_controversial_sampled_1,sep=',', encoding='utf-8',quoting=csv.QUOTE_ALL)

    controversial_topic_counts = []
    for topic in controversial_topics:
        topic_df = controversy_questions_df[controversy_questions_df['question'].str.contains(topic)]
        count= len(topic_df)
        controversial_topic_counts.append(count)

    bins = range(0,10000,100)
    fig, ax = plt.subplots()
    hist = ax.hist(controversial_topic_counts, bins, histtype='bar', rwidth=0.8)
    print(len(hist[0]),len(hist[1]))
    frequencies = hist[0].tolist()
    frequencies.append(-111)
    topic_counts = hist[1].tolist()
    histogram_df = pd.DataFrame({'topic-counts':topic_counts,'frequencies':frequencies})
    histogram_path= get_histogram_path("yahoo","topics")
    histogram_figure_path= get_histogram_path_figure("yahoo","topics")
    histogram_df.to_csv(histogram_path,sep=',',encoding='utf-8')
    print(histogram_figure_path)
    fig.savefig(histogram_figure_path)

#write_yahoo_controversial_topics_statistics()

write_yandex_controversial_topic_statistics()

import pandas as pd
from conf.configuration import *
import json
path_sampled_controversial_topics = get_source_path('yandex-top-topics-2')
path_questions_over_topic_histogram = get_histogram_path("yandex-top-topics-2","topic")
def write_questions():
    with open(path_sampled_controversial_topics, 'r', encoding='utf8') as json_file:
        data = json.load(json_file)
        phrases=[]
        questions_counts=[]
        for key in data.keys():
            phrases.append(key)
            questions_counts.append(len(data[key]))
        questions_over_topic_histogram=pd.DataFrame({"phrases":phrases,"questions-count":questions_counts})
        questions_over_topic_histogram.to_csv(path_questions_over_topic_histogram,sep=",",encoding="utf-8")

write_questions()
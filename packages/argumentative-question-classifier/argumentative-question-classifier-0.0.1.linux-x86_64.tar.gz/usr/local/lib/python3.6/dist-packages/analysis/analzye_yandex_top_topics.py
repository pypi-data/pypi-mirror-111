import pandas as pd
from conf.configuration import *

def get_per_topic_histogram():
    path_preprocessed= get_preprocessed_path('yandex-topics',1)
    print(path_preprocessed)
    df_preprocessed_questions =pd.read_csv(path_preprocessed,sep="\t",encoding="utf-8")
    per_topic_aggregated=df_preprocessed_questions['topic'].value_counts()
    print(per_topic_aggregated.to_string())

get_per_topic_histogram()
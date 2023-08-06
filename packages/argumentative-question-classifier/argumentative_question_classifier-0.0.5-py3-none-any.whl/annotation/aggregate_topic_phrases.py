from conf.configuration import *
import pandas as pd
path_topic_expanded = get_path_expanded('top-topics')
df_topics_expanded = pd.read_csv(path_topic_expanded,sep=",",encoding='utf-8')
topic_phrases_aggregated=df_topics_expanded.groupby('topic').agg({'phrase':lambda x: " ; ".join(list(x))})
topic_phrases_aggregated.to_csv("/mnt/ceph/storage/data-in-progress/questions-taxonomy/top-topics/top-topics-expanded-for-better-descriptions.csv")
print(topic_phrases_aggregated.to_string())
print(path_topic_expanded)
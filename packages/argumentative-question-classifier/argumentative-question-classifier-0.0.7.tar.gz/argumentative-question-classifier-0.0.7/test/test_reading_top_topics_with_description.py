from conf.configuration import *
import pandas as pd
def load_topic_description_df():
    path_topic_description = get_path_described_topics('top-topics')
    df_topics_with_description= pd.read_csv(path_topic_description,sep="\t",encoding='utf-8')
    df_topics_with_description['topic']=df_topics_with_description.apply(lambda topic: topic['topic'].strip(),axis=1)
    return df_topics_with_description


df = load_topic_description_df()
print(df['Russian-article'].to_string())
import pandas as pd
import re
from conf.configuration import *
path_english_wikipedia_click_stream_1 = get_english_wikipedia_clikcstream_path(2015,1)
path_english_wikipedia_click_stream_2 = get_english_wikipedia_clikcstream_path(2015,2)
path_english_wikipedia_click_stream_3 = get_english_wikipedia_clikcstream_path(2016,2)
path_english_wikipedia_click_stream_4 = get_english_wikipedia_clikcstream_path(2016,3)
path_english_wikipedia_click_stream_5 = get_english_wikipedia_clikcstream_path(2016,4)
path_english_wikipedia_click_stream_6 = get_english_wikipedia_clikcstream_path(2016,8)
path_english_wikipedia_click_stream_7 = get_english_wikipedia_clikcstream_path(2016,9)
path_english_wikipedia_click_stream_8 = get_english_wikipedia_clikcstream_path(2017,1)
def prepare_wikipedia_click_stream_pathes():
    pathes=[]
    for month in range(1,3):
       path= get_english_wikipedia_clikcstream_path(2015,month)
       pathes.append(path)
    for month in range(2,5):
       path= get_english_wikipedia_clikcstream_path(2016,month)
       pathes.append(path)
    for month in range(8,10):
        path= get_english_wikipedia_clikcstream_path(2016,month)
        pathes.append(path)
    path=get_english_wikipedia_clikcstream_path(2017,1)
    pathes.append(path)
    return pathes
pathes = prepare_wikipedia_click_stream_pathes()

all_click_stream_df=None
first_initialization=True
for path in pathes:
    if first_initialization:
        first_initialization=False
        all_click_stream_df = pd.read_csv("/mnt/nfs/webis20/data-in-progress/wikipedia-clickstream/2015_02_en_clickstream.tsv", sep='\t', header=0)
    else:
        new_click_stream_df = pd.read_csv("/mnt/nfs/webis20/data-in-progress/wikipedia-clickstream/2015_02_en_clickstream.tsv", sep='\t', header=0)
        all_click_stream_df=pd.concat([all_click_stream_df,new_click_stream_df])
#we won't use ids here, so lets discard them
all_click_stream_df = all_click_stream_df[['prev_title', 'curr_title', 'n', 'type']]
all_click_stream_df.columns = ['prev', 'curr', 'n', 'type']
all_click_stream_df=all_click_stream_df.dropna()
path_wikipedia_controversial_topics = "/mnt/nfs/webis20/data-in-progress/questions-taxonomy/wikipedia-controversial-topics/wikipedia-controversial-issues.txt"
def load_controversial_topics():
    topics= []
    wikipedia_controversial_topics_file = open(path_wikipedia_controversial_topics,encoding='utf-8')
    for line in wikipedia_controversial_topics_file:
        print(line)
        topics.append(line.lower().strip())
    return topics
def build_controversial_topics_regexp(controversial_topics):
    controversial_topics_with_braces=["^("+topic+")$" for topic in controversial_topics]
    return  '|'.join(controversial_topics_with_braces)
controversial_topics = load_controversial_topics()
for topic in controversial_topics:
    print(topic)
controversial_topics_regexp = build_controversial_topics_regexp(controversial_topics)
all_click_stream_df=all_click_stream_df[all_click_stream_df['prev'].str.match('other-google')]
all_click_stream_df['curr']=all_click_stream_df['curr'].str.lower()
controversial_questions_dataset = all_click_stream_df[all_click_stream_df['curr'].str.match(controversial_topics_regexp)]
path_with_clickstream=get_wikipedia_controversial_topics_path('with_clickstream')
controversial_topics_with_clickstreams_df = controversial_questions_dataset.groupby('curr').sum().sort_values('n', ascending=False)[:50]
controversial_topics_with_clickstreams_df.to_csv(path_with_clickstream,sep=",",encoding="utf-8")
print(controversial_topics_with_clickstreams_df.to_string())
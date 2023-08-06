import pandas as pd
from conf.configuration import *
path_topics_expanded = get_path_expanded("top-topics")
import json
path_yandex_source = get_source_path("yandex-top-topics")
path_topics_described=get_path_described_topics("top-topics")

def do_we_have_description_for_all_matched_topics():
    topics_described_df=pd.read_csv(path_topics_described, sep='\t', encoding='utf-8')
    described_topics=list(topics_described_df['topic'])

    topics_expanded_df=pd.read_csv(path_topics_expanded,sep=",",encoding="utf-8")
    expanded_topics=list(topics_expanded_df['topic'])
    print(len(list(set(expanded_topics))))
    print(len(list(set(described_topics))))
    for topic in described_topics:
        if topic not in expanded_topics:
            print(topic)
def are_all_pharses_there():
    topics_expanded_df=pd.read_csv(path_topics_expanded, sep=',', encoding='utf-8')
    phrases=list(topics_expanded_df['phrase'])
    lowered_phrases = [phrase.lower() for phrase in phrases]
    with open(path_yandex_source, 'r', encoding='utf8') as json_file:
        data = json.load(json_file)
        json_file.close()
        for key in data.keys():
            if key.lower() not in lowered_phrases:
                print(key)

are_all_pharses_there()
do_we_have_description_for_all_matched_topics()
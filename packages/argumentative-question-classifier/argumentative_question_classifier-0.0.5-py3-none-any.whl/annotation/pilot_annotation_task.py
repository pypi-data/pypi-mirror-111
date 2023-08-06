import pandas as pd
from conf.configuration import *

def generate_annotations_task():
    path_yandex_top_topics = get_sampled_path('yandex-top-topics')
    df_yandex_topic_topics = pd.read_csv(path_yandex_top_topics,encoding="utf-8",sep="\t", index_col="question-id")
    questions=df_yandex_topic_topics.copy()
    questions=questions[['question','topic']]
    empty = ["" for question in list(questions['question'])]
    questions['argumentative']=empty
    questions["factoid"]=empty
    questions["method"]=empty
    questions["others"]=empty
    questions["opinion"]=empty
    questions["not-question"]=empty
    questions["not-on-topic"]=empty
    return questions

def generate_annotations_task_nordstream():
    path_top_topics_nord_stream = get_sampled_path_pattern('yandex-top-topics','nordstream')
    df_yandex_sample_nordstream = pd.read_csv(path_top_topics_nord_stream,encoding="utf-8",sep="\t", index_col="question-id")
    questions=df_yandex_sample_nordstream.copy()
    questions=questions[['question','topic']]
    empty = ["" for question in list(questions['question'])]
    questions['argumentative']=empty
    questions["factoid"]=empty
    questions["method"]=empty
    questions["others"]=empty
    questions["opinion"]=empty
    questions["not-question"]=empty
    questions["not-on-topic"]=empty
    return questions

def generate_annotations_task_for(annotator):
    path_annotator = get_pilotstudy_annotator_path('pilot-study-top-topics-sample',annotator)
    df_yandex_top_topics_annotation_task = generate_annotations_task_nordstream()
    df_yandex_top_topics_annotation_task.to_csv(path_annotator,sep="\t",encoding="utf-8")

def generate_nordstream_annotations_tasks_for(annotator):
    path_annotator = get_pilotstudy_annotator_path_part('pilot-study-top-topics-sample-corrected',annotator,'nordstream')
    df_nordstream_annotations = generate_annotations_task_nordstream()
    df_nordstream_annotations.to_csv(path_annotator,sep="\t",encoding="utf-8")

generate_nordstream_annotations_tasks_for("sascha")
generate_nordstream_annotations_tasks_for("pavel")

#generate_annotations_task_for("sascha")
#generate_annotations_task_for("pavel")
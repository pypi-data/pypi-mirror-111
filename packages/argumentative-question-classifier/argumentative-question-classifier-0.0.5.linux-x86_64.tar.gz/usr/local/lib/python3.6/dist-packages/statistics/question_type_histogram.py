import pandas as pd
from conf.configuration import *

from conf.configuration import get_pilotstudy_dataset_agreed_path
import matplotlib.pyplot as plt


def get_translated_topics():
    path_translated_topics = get_translated_path('top-topics')
    df_translated_topics= pd.read_csv(path_translated_topics ,encoding='utf-8',error_bad_lines=False)
    return df_translated_topics


def annotation_to_label(label):
    if label == 0:
        return 'fact'
    elif label == 1:
        return 'method'
    elif label == 2:
        return 'arg'
    elif label == 3:
        return 'not-question'
    elif label == 4:
        return 'not-topic'
    elif label == 5:
        return 'others'
    else:
        return 'no-agreement'

def annotation_to_label_on_topic(label):
    if label==0:
        return 'fact'
    elif label==1:
        return 'method'
    elif label==2:
        return 'argument'

def translate(russian_topic):
    if russian_topic =='ЭКО':
        return 'ECO'
    elif russian_topic == 'легализация марихуаны':
        return 'Legalization of marijuana'
    elif russian_topic == 'наводнение в Крымске':
        return 'Flood in Krymsk '
    elif russian_topic == 'президентские выборы в России':
        return 'Presidential elections in Russia '
    elif russian_topic == 'протесты в России':
        return 'Protests in Russia '
    elif russian_topic == 'северный поток':
        return 'North stream '
    elif russian_topic == 'легализация марихуаны':
        return 'Legalization of marijuana'
    elif russian_topic =='смертная казнь':
        return 'Death penalty'
    elif russian_topic =='эвтаназия':
        return 'Euthanasia'

def count_questions_per_types_over_topic(study):
    if study== 'pilot-study-top-topics-sample':
        path_question_dataset = get_pilotstudy_dataset_agreed_path(study)
    elif study=='question-categories':
        path_question_dataset = get_path_part(study,'production-labels-merged')
    else:
        path_question_dataset= get_preprocessed_path("yandex-top-topics-all", 3)


    df_translated_topics = get_translated_topics()

    path_histogram_question_type_over_topic = get_histogram_path_over(study,'question_type','topic')
    df_questions_dataset = pd.read_csv(path_question_dataset,sep='\t',encoding='utf-8')

    fig, axes = plt.subplots(nrows=5, ncols=4)
    fig.tight_layout()
    row_counter = 0
    column_counter = 0
    if study=='pilot-study-top-topics-sample':
        df_questions_dataset['label']= df_questions_dataset.apply(lambda x:annotation_to_label(x['annotation']),axis=1)
    else:
        df_questions_dataset=df_questions_dataset[df_questions_dataset['annotation']!=-1]
        df_questions_dataset['label']= df_questions_dataset.apply(lambda x:annotation_to_label_on_topic(x['annotation']),axis=1)

    df_questions_dataset['label']=df_questions_dataset['label'].astype(str)
    for topic, df_sample_top_topics_questions_per_topic in df_questions_dataset.groupby('topic'):
        translated_topic=df_translated_topics['english-topic'].loc[df_translated_topics['topic'].astype(str).str.match(topic)]
        if translated_topic.count()==0:
            displayed_topic=translate(topic)
            print(topic)
        else:
            displayed_topic=str(translated_topic.iloc[0])
        displayed_topic=displayed_topic.title()
        df= df_sample_top_topics_questions_per_topic[['question','annotation','label']].groupby('label',as_index=False).count()
        df.plot.bar(ax=axes[row_counter,column_counter],x='label',y='question',ylabel='#question',xlabel="",label=str(displayed_topic),yticks=range(0,5000,1000),title=displayed_topic,legend=False,sort_columns=True)
        axes[row_counter,column_counter].set_xticklabels(axes[row_counter,column_counter].get_xticklabels(), rotation=0)
        column_counter = column_counter +1
        if column_counter==4:
            column_counter=0
            row_counter= row_counter+1


    fig.set_size_inches(15.5, 10.5)
    fig.savefig(path_histogram_question_type_over_topic,bbox_inches='tight')
#count_questions_per_types_over_topic("pilot-study-top-topics-sample")
#count_questions_per_types_over_topic("question-categories")
count_questions_per_types_over_topic('yandex-top-topics-all')




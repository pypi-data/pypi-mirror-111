import pandas as pd
from conf.configuration import *
import csv

def validate_topics_description_df():
    path_corrected_final=get_preprocessed_path('pilot-study-top-topics-sample-corrected',2)
    df = pd.read_csv(path_corrected_final,sep="\t",encoding='utf-8')
    df_value_counts= df['topic'].value_counts()
    print(df_value_counts.to_string())
    print(path_corrected_final)
validate_topics_description_df()

def load_topic_description_df():
    path_topic_description = get_path_described_topics('top-topics')
    df_topics_with_description= pd.read_csv(path_topic_description,sep="\t",encoding='utf-8')
    df_topics_with_description['topic']=df_topics_with_description.apply(lambda topic: topic['topic'].lower().strip(),axis=1)
    return df_topics_with_description

def get_hints():
    hints = {}
    hints[0]= 'Ответ на вопрос – это уникальный факт, с которым согласно большинство людей.'
    hints[1]= 'Ответ на вопрос – инструкция или описание метода для достижения цели/решения задачи.'
    hints[2]= 'Ответ на вопрос – аргументы в пользу или против позиции, принятия решения или совершения действия. С большой вероятностью мнения людей по вопросу расходятся.'
    hints[3]= 'Представленный текст не является вопросом.'
    hints[4]= 'Вопрос не связан с данной темой.'
    hints[5]= 'Несерьезный, непонятный или тривиальный вопрос, не относящийся к одной из вышеописанных категорий.'
    hints[6]='Ответ на вопрос – субъективное мнение/впечатление/эмоция.'
    return hints

def generate_training_annotation_tasks():

    path_agreed_questions= get_pilotstudy_dataset_agreed_path('pilot-study-top-topics-sample')
    path_training = get_path_part('pilot-study-top-topics-sample', 'training')
    df_questions_agreed = pd.read_csv(path_agreed_questions,encoding='utf-8',sep="\t")
    df_questions_agreed.info()
    hints = get_hints()
    df_death_penalty_questions = df_questions_agreed.loc[df_questions_agreed['topic']=='смертн казн',:]
    df_death_penalty_questions_with_argeement = df_death_penalty_questions.loc[df_death_penalty_questions['annotation']!=-1]
    df_topic_description=load_topic_description_df()
    df_death_penalty_questions_with_description=pd.merge(df_death_penalty_questions_with_argeement,df_topic_description[['Russian-description','topic']],on='topic',how='left')
    df_death_penalty_questions_with_description['hint']=df_death_penalty_questions_with_description.apply(lambda question: hints[int(question['annotation'])],axis=1)
    df_death_penalty_questions_with_agreement_toloka  = df_death_penalty_questions_with_description[['question','question-id','annotation','Russian-description','hint']].rename(columns={"Russian-description":"INPUT:topic-description",'question-id':"INPUT:id","question":"INPUT:question","annotation":"GOLDEN:category","hint":'HINT:text'})
    df_death_penalty_questions_with_agreement_toloka.to_csv(path_training,sep='\t', encoding='utf-8',index=False)

def get_quality_annotations_dataframe():
    path_agreed_questions= get_pilotstudy_dataset_agreed_path('pilot-study-top-topics-sample')
    df_questions_agreed = pd.read_csv(path_agreed_questions,encoding='utf-8',sep="\t")
    qf_questions_agreed_without_death_penalty =  df_questions_agreed.loc[df_questions_agreed['topic']!='смертн казн',:]
    df_questions_with_majority=  qf_questions_agreed_without_death_penalty.loc[qf_questions_agreed_without_death_penalty['annotation']!=-1]
    sampled_annotated_questions = df_questions_with_majority.loc[df_questions_with_majority['annotation']!=-1].sample(n=200)
    return sampled_annotated_questions

def generate_annotation_task():
    path_yandex_sampled_top_topics = get_sampled_path('yandex-top-topics')
    path_pilot_study_toloka = get_pilotstudy_dataset_toloka_path('pilot-study-top-topics-sample')
    path_pilot_study_toloka_batches = get_path_part('pilot-study-top-topics-sample', 'batches')
    questions_df = pd.read_csv(path_yandex_sampled_top_topics,encoding="utf-8",sep="\t")
    questions_df_without_death_penalty = questions_df.loc[questions_df['topic']!='смертн казн',:]
    questions_df_without_death_penalty=questions_df_without_death_penalty[['question-id','question','topic']]
    questions_df_without_death_penalty['topic']=questions_df_without_death_penalty.apply(lambda question: question['topic'].lower().strip(),axis=1)

    df_topic_description=load_topic_description_df()
    df_question_with_description=pd.merge(questions_df_without_death_penalty,df_topic_description[['Russian-description','topic']],on='topic',how='left')
    df_question_with_description=df_question_with_description.sort_values(['topic','question-id'])
    last_question_id_per_topic = df_question_with_description.copy().groupby('topic')['question-id'].max()
    del df_question_with_description['topic']
    df_sampled_annotated_questions  = get_quality_annotations_dataframe()

    df_question_with_quality_checks=pd.merge(df_question_with_description,df_sampled_annotated_questions[['question-id','annotation']],on='question-id',how='left')
    questions_toloka_df = df_question_with_quality_checks[['question','question-id','Russian-description','annotation']].rename(columns={'question-id':"INPUT:id","question":"INPUT:question","Russian-description":"INPUT:topic-description","annotation":"GOLDEN:category"})

    path_pilot_study_toloka_batches = get_path_part('pilot-study-top-topics-sample', 'batches')
    questions_toloka_df['GOLDEN:category']=questions_toloka_df['GOLDEN:category'].fillna(-1).astype(int)
    questions_toloka_df['GOLDEN:category'].loc[questions_toloka_df['GOLDEN:category']==-1]=""
    questions_toloka_df.to_csv(path_pilot_study_toloka,columns=['INPUT:id','INPUT:question','INPUT:topic-description','GOLDEN:category'],sep="\t",encoding="utf-8",index=False)
    questions_toloka_df.info()
    skip_header=False

    with open(path_pilot_study_toloka,'r') as file_annotation_tasks:
        with open(path_pilot_study_toloka_batches,'w') as file_annotation_tasks_batches:
            for line in file_annotation_tasks:
                if not skip_header:
                    file_annotation_tasks_batches.write(line)
                    skip_header=True
                    continue
                question_id = line.split('\t')[0]
                if int(question_id) in list(last_question_id_per_topic):
                    file_annotation_tasks_batches.write(line+"\n")
                else:
                    file_annotation_tasks_batches.write(line)









# for question_id in list(question_ids):
#     if line.startswith(str(question_id)):
#         file_annotation_tasks_batches.write(line+"\n")
#         continue
# file_annotation_tasks_batches.write(line)


# def generate_annotations_task():
#     path_yandex_top_topics_death_penalty = get_sampled_path_pattern('yandex-top-topics','death_penalty')
#     path_pilot_study_toloka = get_pilotstudy_dataset_toloka_path('pilot-study-top-topics-subsample')
#     print(path_yandex_top_topics_death_penalty)
#     print(path_pilot_study_toloka)
#     yandex_queries_df = pd.read_csv(path_yandex_top_topics_death_penalty,sep='\t',encoding="utf-8")
#     yandex_queries_with_annotation = yandex_queries_df.loc[yandex_queries_df['annotation']!=-1].sample(n=10)
#     yandex_queries_df['annotation']=None
#     yandex_queries_df.loc[yandex_queries_with_annotation.index,'annotation']=yandex_queries_with_annotation['annotation']
#     yandex_queries_df[['question','question-id','annotation']].rename(columns={'question-id':"INPUT:id","question":"INPUT:question","annotation":"GOLDEN:category"}).to_csv(path_pilot_study_toloka,sep='\t', encoding='utf-8',index=False)


#generate_dataset()
#generate_annotation_task()
#generate_training_annotation_tasks()
import nltk
import pandas as pd
from conf.configuration import *
from sklearn.metrics import cohen_kappa_score
def calculate_agreement():
    indices_1,annotations_1 = read_annotations('sascha')
    indices_2,annotations_2 = read_annotations('pavel')
    common_indices= set(indices_1).intersection(set(indices_2))
    filtered_annotations_1 = [annotations_1[i] for i,index in enumerate(indices_1) if index in common_indices ]
    filtered_annotations_2 = [annotations_2[i] for i,index in enumerate(indices_2) if index in common_indices ]
    #confusion_matrix=create_confusion_matrix(filtered_annotations_1,filtered_annotations_2)
    #confusion_matrix_path = get_pilotstudy_dataset_analysis("pilot-study-top-topics-sample","confusion-matrix")
    #confusion_matrix = confusion_matrix[["labels","factoid","method","argumentative","others","not-question","not-on-topic","no-choice"]]
    #confusion_matrix.to_csv(confusion_matrix_path,sep=",",header=True,columns=["labels","factoid","method","argumentative","not-question","not-on-topic","others","no-choice"])
    kappa_score = cohen_kappa_score(filtered_annotations_1,filtered_annotations_2)
    print("cohen_kappa is %f" %kappa_score)

def get_translated_topics():
    path_translated_topics = get_translated_path('top-topics')
    df_translated_topics= pd.read_csv(path_translated_topics ,encoding='utf-8',error_bad_lines=False)
    return df_translated_topics

def calculate_agreement_per_topic():
    df_translated_topics = get_translated_topics()


    path_agreement_per_topic = pilot_study_agreement_per_topic_path('pilot-study-top-topics-sample')
    df_sascha_annotations = read_annotations_data_frame('sascha')
    df_pavel_annotations = read_annotations_data_frame('pavel')
    topics = []
    agreements = []
    agreement_per_topic_columns={}
    for topic,df_sascha_annotations_per_topic in df_sascha_annotations.groupby('topic'):
        translated_topic=df_translated_topics['english-topic'].loc[df_translated_topics['topic'].astype(str).str.match(topic)]
        topics.append(str(translated_topic.to_string()))
        df_pavel_annotations_per_topic=df_pavel_annotations.loc[df_sascha_annotations_per_topic.index]
        sascha_indices,sascha_annotations = parse_annotations(df_sascha_annotations_per_topic)
        pavel_indices,pavel_annotations=  parse_annotations(df_pavel_annotations_per_topic)
        kappa_score = cohen_kappa_score(sascha_annotations,pavel_annotations)
        agreements.append(kappa_score)
    agreement_per_topic_columns['topic']=topics
    agreement_per_topic_columns['agreement']=agreements
    df_agreement_per_topic= pd.DataFrame(agreement_per_topic_columns)
    df_agreement_per_topic.to_csv(path_agreement_per_topic,sep="\t",encoding="utf-8")



def create_confusion_matrix(annotations_1,annotations_2):
    labels=["factoid","method","argumentative","not-question","not-on-topic","others","no-choice"]
    confusion_matrix=[]
    for index in range(0,7):
        confusion_matrix.append([])
        for j in range(0,7):
            confusion_matrix[index].append(0)
    for i,annotation_1 in enumerate(annotations_1):
        annotation_2 = annotations_2[i]
        confusion_matrix[annotation_1][annotation_2]=confusion_matrix[annotation_1][annotation_2]+1
    inter_annotator_agreement = pd.DataFrame({"labels":labels,"factoid":confusion_matrix[0],"method":confusion_matrix[1],"argumentative":confusion_matrix[2],"not-question":confusion_matrix[3],"not-on-topic":confusion_matrix[4],"others":confusion_matrix[5],'no-choice':confusion_matrix[6]})

    return inter_annotator_agreement

def generate_annotations_task():
    path_yandex_top_topics = get_sampled_path('yandex-top-topics')
    df_yandex_topic_topics = pd.read_csv(path_yandex_top_topics,encoding="utf-8",sep="\t", index_col="question-id").sort_index()
    questions=df_yandex_topic_topics.copy()
    questions=questions[['question','topic']]
    empty = ["" for question in list(questions['question'])]
    questions['argumentative']=empty
    questions["factoid"]=empty
    questions["method"]=empty
    questions["others"]=empty
    questions["not-question"]=empty
    questions["not-on-topic"]=empty

def read_annotations(annotator):
    path_annotator = get_pilotstudy_annotator_path_version('pilot-study-top-topics-sample',annotator,'done',3)
    annotations_df = pd.read_csv(path_annotator,encoding="utf-8",sep="\t", index_col="question-id").sort_index()
    annotations = parse_annotations(annotations_df)
    return annotations

def read_annotations_data_frame(annotator,include_index=False):
    path_annotator = get_pilotstudy_annotator_path_part('pilot-study-top-topics-sample',annotator,'done')
    if not include_index:
        annotations_df = pd.read_csv(path_annotator,encoding="utf-8",sep="\t", index_col="question-id").sort_index()
    else:
        annotations_df = pd.read_csv(path_annotator,encoding="utf-8",sep="\t")
    return annotations_df

def read_completed_missing_annotations_data_frame(annotator):
    path_annotator= get_pilotstudy_annotator_path_part('pilot-study-top-topics-sample',annotator,'missing_done')
    annotations_df = pd.read_csv(path_annotator,encoding="utf-8",sep="\t")
    return annotations_df

def read_completed_argumentative_others_data_frame(annotator):
    path_annotator= get_pilotstudy_annotator_path_part('pilot-study-top-topics-sample',annotator,'argumentative_others_completed')
    annotations_df = pd.read_csv(path_annotator,encoding="utf-8",sep="\t")
    return annotations_df


def parse_annotations(annotation_df):
    annotations_df = annotation_df.sort_index()

    indices = list(annotations_df.index)
    questions = list(annotations_df['question'])
    is_factoid=list(annotations_df['factoid'])
    not_question=list(annotations_df['not-question'])
    not_on_topic=list(annotations_df['not-on-topic'])
    is_argumentative=list(annotations_df['argumentative'])
    others = list(annotations_df['others'])
    is_method =list(annotations_df['method'])
    is_opinion =list(annotations_df['opinion'])
    annotations=[]
    for i,question in enumerate(questions):
        try:
            annotation =boolean_to_int_with_opinion(is_factoid[i],is_method[i],is_argumentative[i],others[i],not_question[i],not_on_topic[i],is_opinion[i])
            annotations.append(annotation)
        except Exception as error:
                print(error)
                None
    return indices,annotations
def string_to_int(label):
    if label == 'factoid':
        return 0
    elif label == 'method':
        return 1
    elif label == 'argumentative':
        return 2
    elif label == 'not-question':
        return 3
    elif label == 'not-on-topic':
        return 4
    elif label == 'others':
        return 5
    else:
        return 6

def string_to_int_with_opinion(label):
    if label == 'factoid':
        return 0
    elif label == 'method':
        return 1
    elif label == 'argumentative':
        return 2
    elif label == 'not-question':
        return 3
    elif label == 'not-on-topic':
        return 4
    elif label == 'others':
        return 5
    elif label=='opinion':
        return 6
    else:
        return 7


def boolean_to_int(is_factoid,is_method,is_argumentative,others,not_question,not_on_topic):
    if is_factoid==1.0 or (isinstance(is_factoid,str) and 't' in is_factoid):
        return 0
    elif is_method==1.0 or  (isinstance(is_method,str) and 't' in is_method):
        return 1
    elif is_argumentative==1.0 or  (isinstance(is_argumentative,str)and 't'in is_argumentative ):
        return 2
    elif not_question==1.0 or (isinstance(not_question,str) and 't' in not_question):
        return  3
    elif not_on_topic==1.0 or (isinstance(not_on_topic,str) and 't' in not_on_topic):

        return 4
    elif others==1.0 or (isinstance(others,str) and 't' in others):
        return 5
    else:
        return 6

def boolean_to_int_with_opinion(is_factoid,is_method,is_argumentative,others,not_question,not_on_topic,is_opinion):
    if is_factoid==1.0 or (isinstance(is_factoid,str) and 't' in is_factoid):
        return 0
    elif is_method==1.0 or  (isinstance(is_method,str) and 't' in is_method):
        return 1
    elif is_argumentative==1.0 or  (isinstance(is_argumentative,str)and 't'in is_argumentative ):
        return 2
    elif not_question==1.0 or (isinstance(not_question,str) and 't' in not_question):
        return  3
    elif not_on_topic==1.0 or (isinstance(not_on_topic,str) and 't' in not_on_topic):

        return 4
    elif others==1.0 or (isinstance(others,str) and 't' in others):
        return 5
    elif is_opinion==1.0 or (isinstance(is_opinion,str) and 't' in is_opinion):
        return 6
    else:
        return 7

def create_confusion_analysis_list_for_labels(pavel_label,sascha_label):
    indices_sascha,annotations_sascha = read_annotations('sascha')
    indices_pavel,annotations_pavel = read_annotations('pavel')
    common_indices= set(indices_sascha).intersection(set(indices_pavel))
    common_indices_list = sorted(list(common_indices))
    pavel_label_int = string_to_int(pavel_label)
    sascha_label_int = string_to_int(sascha_label)
    filtered_annotations_sascha = [annotations_sascha[i] for i,index in enumerate(indices_sascha) if index in common_indices ]
    filtered_annotations_pavel = [annotations_pavel[i] for i,index in enumerate(indices_pavel) if index in common_indices ]
    both_annotations_with_indices = list(zip(filtered_annotations_pavel,filtered_annotations_sascha,common_indices_list))
    filtered_annotations = list(filter((lambda annotation_with_index: annotation_with_index[0] == pavel_label_int and annotation_with_index[1] == sascha_label_int),both_annotations_with_indices))
    filtered_indices = list(map((lambda annotation_with_index: annotation_with_index[2]),filtered_annotations))
    annotations= read_annotations_data_frame('sascha')
    filtered_annotations = annotations.loc[filtered_indices,:]
    path = get_pilot_study_confusion_analysis('pilot-study-top-topics-sample',pavel_label,sascha_label)
    filtered_annotations.to_csv(path,encoding="utf-8",sep="\t")

def get_non_annotated_questions(annotator):
    indices,annotations= read_annotations(annotator)
    annotations_with_indices = zip(indices,annotations)
    filtered_annotations = filter(lambda annotation: annotation[1]==6,annotations_with_indices)
    indices = list(map(lambda annotation_with_index: annotation_with_index[0],filtered_annotations))
    annotations_df= read_annotations_data_frame(annotator)
    filtered_annotations = annotations_df.loc[indices,:]
    path_missing_annotations = get_pilotstudy_annotator_path_part('pilot-study-top-topics-sample',annotator,'missing')
    filtered_annotations.to_csv(path_missing_annotations,encoding="utf-8",sep="\t")

def merge_non_annotated_questions(annotator):
    df_done = read_annotations_data_frame(annotator,True)
    df_missing_completed = read_completed_missing_annotations_data_frame(annotator)
    path_done_2 = get_pilotstudy_annotator_path_version('pilot-study-top-topics-sample',annotator,'done',2)
    df_done_2 = pd.concat([df_done,df_missing_completed]).drop_duplicates(['question-id'],keep='last')
    df_done_2.to_csv(path_done_2,encoding="utf-8",sep="\t",index=False)

def produce_agreed_questions():
    path_agreed_questions= get_pilotstudy_dataset_agreed_path('pilot-study-top-topics-sample')
    indices_sascha,sascha_annotations = read_annotations('sascha')
    indices_pavel,pavel_annotations = read_annotations('pavel')
    final_annotations=[]
    for i,sascha_annotation in enumerate(sascha_annotations):
        pavel_annotation = pavel_annotations[i]
        if sascha_annotation == pavel_annotation:
            final_annotations.append(sascha_annotation)
        else:
            final_annotations.append(-1)
    df_questions = read_annotations_data_frame('sascha')
    df_questions=df_questions.drop(columns=["factoid","method","others","not-question","argumentative","not-on-topic"])
    df_questions['annotation']=final_annotations
    df_questions.to_csv(path_agreed_questions,encoding="utf-8",sep="\t")
    #calculate_agreement()

def get_argumentative_open_annotations(annotator):
    indices,annotations= read_annotations(annotator)
    annotations_with_indices = zip(indices,annotations)
    argumentative_others_annotations = filter(lambda annotation: (annotation[1]==2 or annotation[1]==5),annotations_with_indices)
    indices = list(map(lambda annotation_with_index: annotation_with_index[0],argumentative_others_annotations))
    annotations_df= read_annotations_data_frame(annotator)
    argumentative_others_df = annotations_df.loc[indices,:]
    argumentative_others_df['opinion']= ["" for annotation in list(indices)]
    path_argumentative_others_annotations = get_pilotstudy_annotator_path_part('pilot-study-top-topics-sample',annotator,'argumentative_others')
    argumentative_others_df.to_csv(path_argumentative_others_annotations,encoding="utf-8",sep="\t")

def merge_opinion_questions_annotations(annotator):
    path_done_2 = get_pilotstudy_annotator_path_version('pilot-study-top-topics-sample',annotator,'done',2)
    df_done_2 = pd.read_csv(path_done_2,sep="\t",encoding="utf-8").sort_values('question-id')
    path_argumentative_others_completed = get_pilotstudy_annotator_path_part('pilot-study-top-topics-sample',annotator,'argumentative_others_completed')
    df_done_2['opinion']=["" for question in list(df_done_2['question'])]
    #df_done_2['not sure']=["" for question in list(df_done_2['question'])]
    df_argumentative_others_completed = pd.read_csv(path_argumentative_others_completed,sep="\t",encoding="utf-8").sort_values('question-id')
    df_done_3= pd.concat([df_done_2,df_argumentative_others_completed]).drop_duplicates(['question-id'],keep='last')
    path_done_3 = get_pilotstudy_annotator_path_version('pilot-study-top-topics-sample',annotator,'done',3)
    df_done_3.to_csv(path_done_3,encoding="utf-8",sep="\t",index=False)


#create_confusion_analysis_list_for_labels('argumentative','factoid')
#create_confusion_analysis_list_for_labels('argumentative','others')
#create_confusion_analysis_list_for_labels('factoid','argumentative')
#create_confusion_analysis_list_for_labels('factoid','not-question')
#create_confusion_analysis_list_for_labels('factoid','not-on-topic')
#create_confusion_analysis_list_for_labels('factoid','others')
#get_non_annotated_questions('pavel')
#get_non_annotated_questions('sascha')
#merge_non_annotated_questions('pavel')
#merge_non_annotated_questions('sascha')
#calculate_agreement_per_topic()
#produce_agreed_questions()
#calculate_agreement_per_topic()
#get_argumentative_open_annotations('pavel')
#get_argumentative_open_annotations('sascha')
#merge_opinion_questions_annotations('pavel')
#merge_opinion_questions_annotations('sascha')
calculate_agreement()
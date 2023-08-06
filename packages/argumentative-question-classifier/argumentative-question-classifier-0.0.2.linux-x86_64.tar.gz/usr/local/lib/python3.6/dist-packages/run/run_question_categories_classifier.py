from argumentative_question_classifier.ruberta_topic import *
from conf.configuration import *
experiment = 'experiment-questions-categories-in-topic'
path_ruberta_topic=get_path_model(experiment,'ruberta-topic')
path_yandex_preprocessed_1 = get_preprocessed_path("yandex-top-topics-all", 1)
df_yandex_questions=pd.read_csv(path_yandex_preprocessed_1,sep="\t",encoding="utf-8")
ruberta = RubertaTopic(num_labels=3,path=path_ruberta_topic,from_dump=True,is_cuda_available=True)
df_yandex_questions['labels']=1

predicted_labels=ruberta.predict(df_yandex_questions)
df_yandex_questions['annotation']=predicted_labels

path_yandex_preprocessed_3 = get_preprocessed_path("yandex-top-topics-all", 3)
df_yandex_questions.to_csv(path_yandex_preprocessed_3,sep="\t",encoding="utf-8")



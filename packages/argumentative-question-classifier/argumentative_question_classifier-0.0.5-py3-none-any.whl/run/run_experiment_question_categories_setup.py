from experiments.experiment_question_categories import *
topics= [topic_id for topic_id in  range(1,22) if topic_id !=16 and topic_id!=8]
experiment_cross_topic='experiment-questions-categories-cross-topic'
experiment_in_topic='experiment-questions-categories-in-topic'

setup_cross_topic_experiment(experiment_cross_topic,topics)
setup_in_topic_experiment(experiment_in_topic,num_splits=5)





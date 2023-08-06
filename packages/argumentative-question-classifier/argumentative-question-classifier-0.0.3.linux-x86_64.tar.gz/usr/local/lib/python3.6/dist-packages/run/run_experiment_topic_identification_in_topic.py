from argumentative_question_classifier.Baseline import RandomBaseline,MajorityBaseline
from conf.configuration import *
from experiments.experiment import *
# from approaches.logistic_regression import LogisticRegressionClassifier
# from approaches.support_vector_machine import SVM
from argumentative_question_classifier.ruberta_topic import RubertaTopic
from argumentative_question_classifier.ruberta import Ruberta
from mylogging import *
experiment = 'experiment-topic-identification-in-topic'

setup_logging(get_path_log(experiment))
scheme={0:"on-topic",1:"not-on-topic"}
pretty_labels = [scheme[key] for key in scheme]
labels=list(scheme.keys())


def run_in_topic_experiment_classifier(classifier, labels, log_split_results=False, log_confusion=True):
    splits=range(0,5)


    df_evaluation_all_splits,confusion_matrix=run_experiment(experiment,splits,labels,question_classifier=classifier)
    df_evaluation_summary = calc_evaluation_summary(df_evaluation_all_splits)

    log_message(f"{experiment}: {classifier}")

    if log_split_results:

        log_evaluation_summary(df_evaluation_all_splits,scheme)
    log_evaluation_summary(df_evaluation_summary,scheme)
    if log_confusion:
        log_matrix(confusion_matrix, pretty_labels, pretty_labels)
    return df_evaluation_summary

def run_in_topic_experiment():
    classifiers=[]
    random_baseline= RandomBaseline(labels)
    majority_baseline = MajorityBaseline()
    df_experiment_results=pd.DataFrame({'classifier':[]})
    # svm = SVM(c=4.84)
    # logistic_regression = LogisticRegressionClassifier(max_iter=500,c=1)
    ruberta_topic = RubertaTopic(num_labels=2)
    ruberta = Ruberta(num_labels=2)
    classifiers.extend([random_baseline,majority_baseline])
    #classifiers.extend([svm,logistic_regression])
    classifiers.extend([ruberta, ruberta_topic])

    for classifier in classifiers:
        df_classifier_evaluation=run_in_topic_experiment_classifier(classifier,labels,log_split_results=False,log_confusion=False)
        df_experiment_results=add_classifier_evaluation(str(classifier),df_classifier_evaluation,df_experiment_results,scheme)
    path_experiment_results=get_path_experiment_results(experiment)
    df_experiment_results.to_csv(path_experiment_results,sep=",",encoding="utf-8",columns=['classifier','label','f1','precision','recall'],index=False)

run_in_topic_experiment()

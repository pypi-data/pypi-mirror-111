from sklearn.metrics import *
from sklearn.metrics import confusion_matrix, classification_report
from collections import namedtuple
import pandas as pd
from mylogging import *
from conf.configuration import *

def load_training_set(experiment, split):
    path_training_split = get_path_experiment_part(experiment, split, 'train')
    return pd.read_csv(path_training_split, sep="\t", encoding="utf-8")


def load_test_set(experiment, split):
    path_test_split = get_path_experiment_part(experiment, split, 'test')
    return pd.read_csv(path_test_split, sep="\t", encoding="utf-8")


def generated_evaluation_type():
    return namedtuple('evaluation', 'f1 p r')


def evaluate_label(df_test, annotations, label):
    Evaluation = generated_evaluation_type()
    f1 = f1_score(df_test.annotation, annotations, average=None, labels=[label])[0]
    p = precision_score(df_test.annotation, annotations, average=None, labels=[label])[0]
    r = recall_score(df_test.annotation, annotations, average=None, labels=[label])[0]
    evaluation = Evaluation(f1, p, r)
    return evaluation


def evaluate_all_labels(df_test, annotations, labels):
    evaluation_results = {}
    for label in labels:
        evaluation = evaluate_label(df_test, annotations, label)
        evaluation_results[label] = evaluation
    return evaluation_results


def evaluate(df_test, annotations):
    Evaluation = generated_evaluation_type()
    f1 = f1_score(df_test.annotation, annotations, average='macro')
    p = precision_score(df_test.annotation, annotations, average='macro')
    r = recall_score(df_test.annotation, annotations, average='macro')
    evaluation = Evaluation(f1, p, r)
    return evaluation


def add_evaluation_split(evaluation_all_splits, split, evaluation_all_labels):
    for label in evaluation_all_labels:
        evaluation_all_splits['split'].append(split)
        evaluation_all_splits['label'].append(label)
        evaluation = evaluation_all_labels[label]
        evaluation_all_splits['precision'].append(evaluation.p)
        evaluation_all_splits['recall'].append(evaluation.r)
        evaluation_all_splits['f1'].append(evaluation.f1)


def run_experiment(experiment, splits, labels, question_classifier):
    evaluation_all_splits = {'split': [], 'label': [], 'f1': [], 'precision': [], 'recall': []}
    true_labels = []
    pred_labels = []

    for split in splits:
        log_message(f"split-{split}")

        df_training = load_training_set(experiment, split)
        df_test = load_test_set(experiment, split)
        question_classifier.fit(df_training)

        predicted_labels = question_classifier.predict(df_test)
        evalaution = evaluate(df_test, predicted_labels)
        evaluation_all_labels = evaluate_all_labels(df_test, predicted_labels, labels)
        evaluation_all_labels['all-labels'] = evalaution
        add_evaluation_split(evaluation_all_splits, split, evaluation_all_labels)
        true_labels.extend(df_test['annotation'])
        pred_labels.extend(predicted_labels)
    df_evaluation_all_splits = pd.DataFrame(evaluation_all_splits)
    confusion_matrix = calc_confustion_matrix(true_labels, pred_labels)
    print(classification_report(true_labels, pred_labels))
    return df_evaluation_all_splits, confusion_matrix,


def calc_evaluation_summary(df_evaluation_all_splits):
    df_summary = pd.DataFrame(columns=df_evaluation_all_splits.columns)
    for label, df_evaluation_all_splits in df_evaluation_all_splits.groupby('label'):
        df_label_sum = df_evaluation_all_splits.sum(axis=0)
        df_label_sum = df_label_sum[['f1', 'precision', 'recall']]
        df_label_sum = df_label_sum / len(df_evaluation_all_splits)
        df_label_sum.loc['split'] = "all-splits"
        df_label_sum.loc['label'] = label
        df_summary = df_summary.append(df_label_sum, ignore_index=True)

    return df_summary


def calc_confustion_matrix(true_labels, pred_labels):
    return confusion_matrix(true_labels, pred_labels)


def add_classifier_evaluation(classifier_label, df_classifier_evaluation, df_experiment_results, scheme):
    if classifier_label in df_experiment_results['classifier'].values:
        df_experiment_results = df_experiment_results[df_experiment_results['classifier'] != classifier_label]
    df_classifier_evaluation['classifier'] = classifier_label
    df_classifier_evaluation['label'] = df_classifier_evaluation['label'].apply(
        lambda label: scheme[label] if label != 'all-labels' else label)
    df_experiment_results = df_experiment_results.append(df_classifier_evaluation)
    return df_experiment_results

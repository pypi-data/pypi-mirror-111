# This script extracts results for the question-annotation-tasks from an MTurk results batch csv file
# and calculates several helpful statistics (fleisskappa, ...)

import csv
import os
from nltk import agreement

# input results from mturk
results_file = "/home/weki3907/Desktop/arguana-question-annotation/Mturk-Output/Batch_214965_batch_results.csv"
output_file = "/home/weki3907/Desktop/arguana-question-annotation/Mturk-Output/Batch_214965_processed.csv"

all_questions = []
all_ids = []
all_answers = []
all_worker_ids = []


# extracts only questions and ids from input results_file
def get_data():
    with open(results_file) as file:
        reader = csv.DictReader(file)
        for row in reader:
            question = row['Input.question']
            q_id = row['Input.id']
            answer = row['Answer.answer']
            worker_id = row['WorkerId']
            all_questions.append(question)
            all_ids.append(q_id)
            all_answers.append(answer)
            all_worker_ids.append(worker_id)


# initializes a dictionary with 0 values
def init_dict():
    dict_ = {}
    for i in range(1, 7, 1):
        dict_[str(i)] = 0
    return dict_


# writes results into the output file.
# WARNING: If the output file already exists it gets deleted
def evaluate_results():
    temp_all_questions = all_questions.copy()
    temp_all_ids = all_ids.copy()
    temp_all_answers = all_answers.copy()
    if os.path.isfile(output_file):
        os.remove(output_file)
        print(" -- Creating new empty file: " + output_file + " --")
    csv_out = open(output_file, "a")
    with csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(["question_id", "question", "factoid", "method", "reason", "argumentative", "opinion", "other"])
        for q in temp_all_questions:
            answer_count = init_dict()
            q_index = temp_all_questions.index(q)
            q_id = temp_all_ids[q_index]
            a = temp_all_answers[q_index]
            answer_count[a] += 1
            temp_all_questions.remove(temp_all_questions[q_index])
            temp_all_ids.remove(temp_all_ids[q_index])
            temp_all_answers.remove(temp_all_answers[q_index])
            for p in temp_all_questions:
                if q == p:
                    p_index = temp_all_questions.index(p)
                    b = temp_all_answers[p_index]
                    answer_count[b] += 1
                    temp_all_questions.remove(temp_all_questions[p_index])
                    temp_all_ids.remove(temp_all_ids[p_index])
                    temp_all_answers.remove(temp_all_answers[p_index])
            csv_list = [q_id, q, answer_count["1"], answer_count["2"], answer_count["3"], answer_count["4"],
                        answer_count["5"], answer_count["6"]]
            writer.writerow(csv_list)
            csv_list.clear()
    print(" -- Writing complete. --")


def calc_fleisskappa_for_3():
    workers = set(all_worker_ids)
    rater1 = ""
    rater2 = ""
    rater3 = ""


def calc_multikappa():
    workers = set(all_worker_ids)
    raters = []
    rater_answers = {}
    while workers:
        raters.append(workers.pop())
    for rater in raters:
        rater_answers[rater] = []
        for i in range(0, len(all_questions)):
            if all_worker_ids[i] == rater:
                rater_answers[rater].append({all_questions[i]: all_answers[i]})
    print(str(rater_answers))

    # debug
    for rater in raters:
        print(len(rater_answers[rater]))
    # For every rater: A list of dicts {question:answer}
    # {rater:[{q:a},{q_2: b},...]}
    # TODO: choose longest rater-dict and iterate over it
    # TODO: then compare to EVERY other rater and if every rater has answered this question q:
    # TODO: add the answer of q from every rater somewhere (dict again?) or calc kappa directly?


get_data()
# evaluate_results()
# calc_fleisskappa_for_3()
calc_multikappa()

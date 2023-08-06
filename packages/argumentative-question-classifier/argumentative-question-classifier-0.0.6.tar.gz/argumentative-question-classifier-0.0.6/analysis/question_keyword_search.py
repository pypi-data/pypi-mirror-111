# This script searches for user-defined words in a user-defined .csv input file
# TODO: The data you need to fill in:
# -> 'input folder' with (only) csv files in it (folders get ignored)
# -> 'search_words' and 'wh_words' can be modified arbitrarily
# -> [optional] 'dataset_names' if you want your plots to have a relevant name
# -> [optional] 'plot_absolute' to True if you want absolute aswell as relative y-axis value plots
# -> [optional] 'topics_path' if you want to search for any topics in your dataset,
#               a list of precompiled popular topics from wikipedia can be found here:
#               https://git.webis.de/arguana/questions-annotation-service/tree/master/controversial_topics
#               'topics_threshold' plots about topics only show topics that appear at least 'threshold' times

import csv
import re
import os
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
from nltk import pos_tag, word_tokenize
import string

# path to folder with input csvs (the csv files have to have a column called 'question')
input_folder = "/home/weki3907/Desktop/arguana-question-annotation/Input-csv/topic_input_csvs/formatted/"

# list of strings only used for plot titles
dataset_names = ["aol"]

# Set to 'True' if you want plots with relative aswell as absolute values on y-axis
# only relative values if 'False'
plot_absolute = True

# list of lowercase words that shall be searched for in all questions
search_words = ["opinion", "argument", "advantage", "disadvantage", "pro", "con"]

# list of lowercase 'wh-words' or question-words
wh_words = ["when", "who", "where", "what", "whom", "whose", "which", "how", "is", "are", "were", "was", "do", "does",
            "would", "can", "will", "could", "should", "by", "with", "to", "in", "at"]

# path for your .txt file of topics (line by line) if you want to search for those; empty string else
topics_path = "/home/weki3907/Desktop/arguana-question-annotation/questions-annotation-service/" \
              "controversial_topics/wikipedia-controversial-issues.txt"

# plots about topics only show topics that appear at least 'threshold' times
topics_threshold = 1


# all occurring questions in the input file
all_questions = []
# dict for plotting the results
plot_data = {}
# keep empty
dataset_name = ""
#
lemmatizer = WordNetLemmatizer()


# fills the lists 'all_questions' with data from the input file
def prepare_data(input_file):
    with open(input_folder + input_file) as file:
        reader = csv.DictReader(file)
        for row in reader:
            question = row['question']
            all_questions.append(question)


# searches for a search_word/string as an individual word as well as a substring in the existing list of all questions
def search_as_substring(search_word, threshold=0):
    matching = [s for s in all_questions if search_word.lower() in s.lower()]
    print("There are " + str(len(matching)) + " questions that include the word: \"" + search_word + "\".")
    if len(matching) >= threshold:
        plot_data[search_word] = len(matching)
    return len(matching)


# searches for a search_word and their plural form (appended "s") as an individual word and not as a substring
def search_as_word(search_word, threshold=0, append_s=True):
    if append_s:
        matching = [s for s in all_questions if (re.search(r'\b' + re.escape(search_word.lower()) + r'\b', s.lower()) or
                                                 re.search(r'\b' + re.escape(search_word + "s") + r'\b', s.lower()))]
    else:
        matching = [s for s in all_questions if (re.search(r'\b' + re.escape(search_word.lower()) + r'\b', s.lower()))]
    # print("There are " + str(len(matching)) + " questions that include the word: \"" +
    #     search_word + "\" or \"" + search_word + "s\".")
    if len(matching) >= threshold:
        plot_data[search_word] = len(matching)
    return len(matching)


# searches for a search_word/string as an individual word as the first word of a question
def search_as_first_word(search_word):
    first_words = []
    for q in all_questions:
        first_words.append(q.split(' ', 1)[0])
    matching = [s for s in first_words if search_word == s.lower()]
    print("There are " + str(len(matching)) + " questions that include the word: \"" + search_word +
          "\" as the first word.")
    plot_data[search_word] = len(matching)


# plots the results for all search words and occurrences (uses the dataset-name for the plot title)
# if parameter 'absolute' is true, both plots with relative values aswell as absolute values on y axis get displayed
def plot(search_word_list):
    all_s_words = search_word_list
    try:
        y_values = [(plot_data[n]/len(all_questions))*100 for n in all_s_words]
    except ZeroDivisionError:
        print("ERROR! No Data found!")
        y_values = [0 for _ in all_s_words]
    plt.plot(all_s_words, y_values, 'k-o')
    plt.xlabel('Search-Words')
    plt.ylabel('Occurrences in %')
    plt.title("Out of " + str(len(all_questions)) + " questions from "
              + dataset_name.capitalize() + "\n (relative values)")
    plt.show()

    if plot_absolute:
        y_values = [plot_data[n] for n in all_s_words]
        plt.plot(all_s_words, y_values, 'k-o')
        plt.xlabel('Search-Words')
        plt.ylabel('Occurrences')
        plt.title("Out of " + str(len(all_questions)) + " questions from "
                  + dataset_name.capitalize() + "\n (absolute values)")
        plt.show()


# searches for all words specified in the list 'search_words'
# function 'prepare_data()' has to be called before calling this
def search_s_words(data_name=""):
    for word in search_words:
        search_as_word(word)
    output_file_name = "s_words_result_" + data_name + ".csv"
    write_to_csv(plot_data, output_file_name)
    plot_data.clear()
    # plot(search_words)


# searches for all words specified in the list 'wh_words'
# function 'prepare_data()' has to be called before calling this
def search_wh_words(data_name=""):
    for wh_word in wh_words:
        search_as_first_word(wh_word)
    output_file_name = "wh_words_result_" + data_name + ".csv"
    write_to_csv(plot_data, output_file_name)
    # plot(wh_words)


# searches for topics specified in 'topics_path' txt file and writes results for each dataset to a csv file
def search_topics(threshold, data_name=""):
    topics = []
    lines = open(topics_path, "r").readlines()
    for line in lines:
        amnt = search_as_word(line.strip(), threshold, False)
        if amnt >= threshold:
            topics.append(line.strip())

    # TODO: add desired path/folder for the resulting csv file here:
    output_file_name = "topics_result_" + data_name + ".csv"
    temp_data = plot_data.copy()
    temp_data["all_topics"] = str(add_dict_vals(plot_data))
    write_to_csv(temp_data, output_file_name)
    # plot(topics)
    print("Questions with at least 1 topic for " + data_name + ": " + str(add_dict_vals(plot_data)))


# writes dict-data to csv file
def write_to_csv(data, output_file):
    with open(output_file, 'w') as f:
        w = csv.writer(f)
        w.writerows(data.items())


# small helper method for adding up values in a dict with string representation of integer values
def add_dict_vals(input_dict):
    total = 0
    for u in input_dict.values():
        total += int(float(u))
    return total


# determines the sentiment (pro, con, neutral) of every question and saves the amount
# of questions with corresponding sentiments in 'positives', 'negatives' and 'neutrals'
def determine_sentiments():
    positives = 0
    negatives = 0
    neutrals = 0
    for q in all_questions:
        s = ''.join(ch for ch in q if ch not in set(string.punctuation))
        token = word_tokenize(s)
        tagged = pos_tag(token)
        sentiment = 0.0
        tokens_count = 0
        for word, tag in tagged:
            wn_tag = penn_to_wn(tag)
            if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
                continue

            lemma = lemmatizer.lemmatize(word, pos=wn_tag)
            if not lemma:
                continue

            synsets = wn.synsets(lemma, pos=wn_tag)
            if not synsets:
                continue

            # Take the first sense, the most common
            synset = synsets[0]
            swn_synset = swn.senti_synset(synset.name())

            sentiment += swn_synset.pos_score() - swn_synset.neg_score()
            tokens_count += 1

            # sum greater than 0 => positive sentiment
        if sentiment > 0:
            positives += 1

            # neutral sentiment
        elif sentiment == 0:
            neutrals += 1

            # negative sentiment
        elif sentiment < 0:
            negatives += 1
    print("Pos: " + str(positives) + "\nand Neg: " + str(negatives) + "\nand neutrals: " + str(neutrals) +
          "\n and total: " + str(negatives + positives + neutrals))


# helper function for sentiments
def penn_to_wn(tag):
    """
    Convert between the PennTreebank tags to simple Wordnet tags
    """
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    elif tag.startswith('V'):
        return wn.VERB
    return None


# main method
def search_everything():
    file_list = [f for f in os.listdir(input_folder)]
    i = 0
    for input_file in file_list:
        if os.path.isfile(input_folder + input_file):
            global dataset_name
            try:
                dataset_name = dataset_names[i]
            except:
                dataset_name = ""
            prepare_data(input_file)
            if topics_path:
                search_topics(topics_threshold, dataset_name)  # search for topics (comment out if not wanted)
            # search_s_words(dataset_name)  # search for s_words (comment out if not wanted)
            # search_wh_words(dataset_name)  # search for wh_words (comment out if not wanted)
            # determine_sentiments()
            plot_data.clear()
            all_questions.clear()
            i += 1


# -- main -- #
search_everything()

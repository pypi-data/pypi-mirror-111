from analysis.pilot_study_question_categorization_analysis import *

for batch in range(1,3):
    acceptance_threshold=0.25
    calc_worker_accuracy('pilot-question-categories',batch)
    calc_inter_annotator_agreement('pilot-question-categories',batch,acceptance_threshold)
    calc_agreed('pilot-question-categories',batch,acceptance_threshold)
    distribution= calc_agreement_distribution('pilot-question-categories',batch)
    #calc_confusion_matrix('pilot-question-categories',batch)
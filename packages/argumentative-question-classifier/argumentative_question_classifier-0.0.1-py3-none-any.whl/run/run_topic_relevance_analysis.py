from analysis.topic_relevance_analysis import *
import logging

logging.basicConfig(filename="../organization/topic-relevance/topic-relevance-results.log", level=logging.DEBUG)
import pandas as pd
batches= range(1,25)


study='topic-relevance'

all_alphas=[]
all_alphas_2nd=[]
all_num_questions=[]

all_num_annotations=[]
all_num_annotations_filtered=[]
all_num_annotations_filtered_2nd_iter=[]

all_num_annotations_without_qc=[]
all_num_annotations_filtered_without_qc=[]
all_num_annotations_filtered_2nd_iter_without_qc=[]

all_num_on_topic=[]
all_num_not_on_topic=[]
all_num_not_a_question=[]
all_num_no_agreement=[]

found_batches=[]
df_questions=pd.DataFrame({'alpha','questions.num','annotations.num','annotation-filtered.num','on-topic','not-on-topic','not-a-question','no-agreement'})
for batch in batches:
    path_batch_results=get_path_part('topic-relevance','batch-%d-results'%batch)
    logging.warning("analyzing batch %d"%batch)
    if path_batch_results!=None and os.path.exists(path_batch_results):
        found_batches.append(batch)
        calc_worker_accuracy(batch,study)
        calc_annotator_per_question_filtered(batch,study)
        calc_annotator_per_question(batch,study)

        alpha = calc_inter_annotator_agreement(batch,study)
        alpha_2nd = calc_inter_annotator_agreement(batch,study,2)
        all_alphas.append(alpha)
        all_alphas_2nd.append(alpha_2nd)

        calc_agreed(batch,study)
        calc_agreed(batch,study,2)

        num_questions, num_annt, num_annt_filtered, num_annt_filtered_2nd, num_annt_without_qc, num_annt_filtered_without_qc, num_annt_filtered_2nd_without_qc = calc_annotation_statistics(batch, study)
        all_num_questions.append(num_questions)
        all_num_annotations.append(num_annt)
        all_num_annotations_filtered.append(num_annt_filtered)
        all_num_annotations_filtered_2nd_iter.append(num_annt_filtered_2nd)

        all_num_annotations_without_qc.append(num_annt_without_qc)
        all_num_annotations_filtered_without_qc.append(num_annt_filtered_without_qc)
        all_num_annotations_filtered_2nd_iter_without_qc.append(num_annt_filtered_2nd_without_qc)

        distribution = calc_agreement_distribution(batch,study,iteration=2)
        all_num_on_topic.append(distribution[0])
        all_num_not_on_topic.append(distribution[1])

        if 2 not in distribution:
            all_num_not_a_question.append(0)
        else:
            all_num_not_a_question.append(distribution[2])

        if -1 not in distribution:
            all_num_no_agreement.append(0)
        else:
            all_num_no_agreement.append(distribution[-1])

for batch in bathces_2nd_iter_final:
    path_batch_results=get_path_part('topic-relevance-2nd','batch-%d-results'%batch)
    logging.warning("analyzing batch %d"%batch)
    if path_batch_results!=None and os.path.exists(path_batch_results):
        found_batches.append(batch)
        alpha_2nd = calc_inter_annotator_agreement(batch,'topic-relevance-2nd',2)
        calc_agreed(batch,'topic-relevance-2nd',2)
        num_questions, num_annt, num_annt_filtered, num_annt_filtered_2nd, num_annt_without_qc, num_annt_filtered_without_qc, num_annt_filtered_2nd_without_qc = calc_annotation_statistics(batch, 'topic-relevance-2nd')
        all_alphas.append(alpha_2nd)
        all_alphas_2nd.append(alpha_2nd)
        all_num_questions.append(num_questions)
        all_num_annotations.append(num_annt)
        all_num_annotations_filtered.append(num_annt_filtered)
        all_num_annotations_filtered_2nd_iter.append(num_annt_filtered_2nd)

        all_num_annotations_without_qc.append(num_annt_without_qc)
        all_num_annotations_filtered_without_qc.append(num_annt_filtered_without_qc)
        all_num_annotations_filtered_2nd_iter_without_qc.append(num_annt_filtered_2nd_without_qc)

        distribution = calc_agreement_distribution(batch,'topic-relevance-2nd',iteration=2)
        all_num_on_topic.append(distribution[0])
        all_num_not_on_topic.append(distribution[1])
        if 2 not in distribution:
            all_num_not_a_question.append(0)
        else:
            all_num_not_a_question.append(distribution[2])

        if -1 not in distribution:
            all_num_no_agreement.append(0)
        else:
            all_num_no_agreement.append(distribution[-1])

df_questions=pd.DataFrame({'batch':found_batches,'alpha-2nd-iter':all_alphas_2nd,'alpha':all_alphas,'questions.num':all_num_questions,'annotations.num':all_num_annotations,
                           'annotations-no-qc.num':all_num_annotations_without_qc,'annotation-filtered.num':all_num_annotations_filtered,'annotations-filtered-no-qc.num':all_num_annotations_filtered_without_qc,
                           'annotations-filtered-2nd.num':all_num_annotations_filtered_2nd_iter,'annotations-filtered-2nd-no-qc.num':all_num_annotations_filtered_2nd_iter_without_qc,'on-topic':all_num_on_topic,
                           'not-on-topic':all_num_not_on_topic,'not-a-question':all_num_not_a_question,'no-agreement':all_num_no_agreement})
df_questions.append(df_questions.sum(),ignore_index=True)
df_questions.to_csv('../organization/topic-relevance/topic-relevance-results.cvs',sep="\t",encoding="utf-8",index=False)
from analysis.question_categorization_analysis import *
study="question-categories"
produce_production_dataset(study)
merge_map={3:2}
produce_production_dataset_merge(study,merge_map)
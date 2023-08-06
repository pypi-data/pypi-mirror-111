from annotation.question_categories import *
study='question-categories'


# don't add_not_annotated_questions(study,True,False)
#sample_quality_checks_for_death_penalty()

prepare_question_categories(study,is_production=True,log_paths=False)

for group in [1,2,3,4]:
    generate_batch(study,group,True,log_paths=False)
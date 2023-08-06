from annotation.question_categories import *
study='question-categories'
path=get_path_log_low_quality(study)
setup_logging(path)
for group in [1,2,3,4]:
    add_low_quality_to_remaining(study,group)
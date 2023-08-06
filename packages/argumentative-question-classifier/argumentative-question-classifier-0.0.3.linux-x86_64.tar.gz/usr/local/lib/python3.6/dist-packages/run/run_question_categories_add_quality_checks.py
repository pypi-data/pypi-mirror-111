from annotation.question_categories import *
study='question-categories'
path=get_path_log_quality_checks(study)
setup_logging(path)
for group in range(1,5):
    add_quality_checks(study,group=group)
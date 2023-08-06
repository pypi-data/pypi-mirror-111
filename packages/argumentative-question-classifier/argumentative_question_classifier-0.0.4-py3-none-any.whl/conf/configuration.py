import os
preprocessed_label_template= "%s_preprocessed_%i"
sampled_label_template = "%s_sampled"
sampled_pattern_label_template = "%s_sampled_%s"
source_label_template = "%s_source"
annotator_study_toloka_label_template= "%s_toloka"
annotator_study_toloka_part_label_template= "%s_toloka_%s"
annotator_study_label_template= "%s_annotator_%s"
annotator_study_label_analysis="%s_analysis_%s"
annotator_study_label_analysis_confusion_template="%s_analysis_confusion"

annotator_study_agreed_label_template="%s-agreed"
annotator_study_label_agreement_per_topic_template="%s_analysis_agreement_per_topic"
annotator_study_label_template_part="%s_annotator_%s_%s"
annotator_study_label_template_part_version="%s_annotator_%s_%s_%d"
sampled_controversial_label_template = "%s_sampled_controversial_topics_%i"
histogram_label_template= "%s_histogram_%s"
histogram_over_label_template="%s_histogram_%s_over_%s"

histogram_label_fig_template= "%s_histogram_%s_fig"
controversial_topic_label_template= "controversial_topics_%s"
annotated_label_template= "%s_annotated_%s_batch_%i"
clickstream_label= "wiki_articles_english_clickstream"
dirname = os.path.dirname(__file__)
expanded_label_template = "%s_expanded"
expanded_2_label_template = "%s_expanded_2"
translated_label_template="%s_translated"
described_label_template="%s_described"
inconsistency_label_template="%s_inconsistency"
label_log_template="%s_log"
label_log_analysis_template="%s_log_analysis"
label_log_quality_checks_template="%s_log_quality-checks"
label_log_low_quality_template="%s_log_low-quality"
label_batches_template="%s_batches"

label_experiment_results="experiment-results"

PROJECT_ROOT = os.path.dirname(__file__) + "/../"

NetworkDriveROOT= '/mnt/ceph/storage/data-in-progress/data-research/arguana/questions-taxonomy/'

def get_dataset_conf_path(dataset_name):
    dataset_conf = dirname+("/%s.conf"%dataset_name)
    return dataset_conf

def get_preprocessed_path(dataset_name,step):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_preprocessed_label = preprocessed_label_template % (dataset_name, step)
    dataset_preprocessed_path = get_property_value(dataset_conf_path,dataset_preprocessed_label)
    return dataset_preprocessed_path

def get_sampled_path(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_sampled_label = sampled_label_template % dataset_name
    dataset_sampled_path = get_property_value(dataset_conf_path,dataset_sampled_label)
    return dataset_sampled_path

def get_path_expanded(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    expanded_label = expanded_label_template%dataset_name
    dataset_expanded_path = get_property_value(dataset_conf_path,expanded_label)
    return dataset_expanded_path

def get_path_expanded_2(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    expanded_label = expanded_2_label_template%dataset_name
    dataset_expanded_path = get_property_value(dataset_conf_path,expanded_label)
    return dataset_expanded_path

def get_translated_path(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    translated_label = translated_label_template%dataset_name
    dataset_translated_path = get_property_value(dataset_conf_path,translated_label)
    return dataset_translated_path

def get_path_described_topics(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    described_label = described_label_template%dataset_name
    dataset_described_path = get_property_value(dataset_conf_path,described_label)
    return dataset_described_path

def get_sampled_path_pattern(dataset_name,pattern):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_sampled_label = sampled_pattern_label_template % (dataset_name,pattern)
    dataset_sampled_path = get_property_value(dataset_conf_path,dataset_sampled_label)
    return dataset_sampled_path

def get_sampled_controversial_path(dataset_name,i):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_sampled_controversial_label = sampled_controversial_label_template % (dataset_name, i)
    dataset_sampled_controversial_path = get_property_value(dataset_conf_path,dataset_sampled_controversial_label)
    return dataset_sampled_controversial_path


def get_source_path(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_source_label = source_label_template % dataset_name
    dataset_source_path = get_property_value(dataset_conf_path,dataset_source_label)
    return dataset_source_path


def get_property_value(dataset_conf_path,property_label):
    conf_file = open(dataset_conf_path,'r')

    for line in conf_file:
        label = line.split("=")[0].strip()
        value = line.split("=")[1].strip()
        if label == property_label:
            if value.startswith("./"):
                return value.replace("./",f"{NetworkDriveROOT}")
            else:
                return value.replace("../", PROJECT_ROOT)

def get_pilotstudy_dataset_toloka_path(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    annotator_study_toloka_label = annotator_study_toloka_label_template%dataset_name
    dataset_toloka_path = get_property_value(dataset_conf_path,annotator_study_toloka_label)
    return dataset_toloka_path

def get_path_part(dataset_name, part):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    annotator_study_toloka_label = annotator_study_toloka_part_label_template%(dataset_name,part)
    dataset_toloka_path = get_property_value(dataset_conf_path,annotator_study_toloka_label)
    return dataset_toloka_path

def get_pilotstudy_annotator_path(dataset_name,annotator):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_annotator_label = annotator_study_label_template % (dataset_name, annotator)
    dataset_annotator_path = get_property_value(dataset_conf_path,dataset_annotator_label)
    return dataset_annotator_path
def get_pilotstudy_annotator_path_part(dataset_name,annotator,part):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_annotator_label = annotator_study_label_template_part % (dataset_name, annotator, part)
    dataset_annotator_path = get_property_value(dataset_conf_path,dataset_annotator_label)
    return dataset_annotator_path

def get_pilotstudy_annotator_path_version(dataset_name,annotator,part,version):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_annotator_label = annotator_study_label_template_part_version % (dataset_name, annotator, part, version)
    dataset_annotator_path = get_property_value(dataset_conf_path,dataset_annotator_label)
    return dataset_annotator_path



def get_pilotstudy_dataset_agreed_path(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    annotator_study_agreed_label= annotator_study_agreed_label_template%(dataset_name)
    path_annotator_study_agreed = get_property_value(dataset_conf_path,annotator_study_agreed_label)
    return path_annotator_study_agreed



def get_pilotstudy_dataset_analysis(dataset_name,analysis):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_analysis_label = annotator_study_label_analysis % (dataset_name,analysis)
    analysis_path = get_property_value(dataset_conf_path,dataset_analysis_label)
    return analysis_path
def get_pilot_study_confusion_analysis(dataset,pavel_label,sascha_label):
    dataset_conf_path = get_dataset_conf_path(dataset)
    annotator_study_label_analysis_confusion_label = annotator_study_label_analysis_confusion_template%dataset
    dataset_annotator_analysis_path_template = get_property_value(dataset_conf_path,annotator_study_label_analysis_confusion_label)
    return dataset_annotator_analysis_path_template%(pavel_label,sascha_label)

def pilot_study_agreement_per_topic_path(dataset):
    dataset_conf_path = get_dataset_conf_path(dataset)
    annotator_study_agreement_per_topic_label = annotator_study_label_agreement_per_topic_template%dataset
    annotator_study_agreement_per_topic_path=  get_property_value(dataset_conf_path,annotator_study_agreement_per_topic_label)
    return annotator_study_agreement_per_topic_path

def get_wikipedia_controversial_topics_path():
    wikipedia_dataset_conf_path=get_dataset_conf_path("wikipedia")
    return get_property_value(wikipedia_dataset_conf_path,'controversial_topics')

def get_wikipedia_controversial_topics_path(property_label):
    wikipedia_dataset_conf_path=get_dataset_conf_path("wikipedia")
    label = controversial_topic_label_template % property_label
    return get_property_value(wikipedia_dataset_conf_path,label)

def get_histogram_path_figure(dataset_name,attribute):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_histogram_attribute_label = histogram_label_fig_template % (dataset_name, attribute)
    dataset_histogram_figure_attribute_path = get_property_value(dataset_conf_path,dataset_histogram_attribute_label)
    return dataset_histogram_figure_attribute_path

def get_histogram_path_over(dataset_name,x,y):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_histogram_label = histogram_over_label_template%(dataset_name,x,y)
    dataset_histogram_path = get_property_value(dataset_conf_path,dataset_histogram_label)
    return dataset_histogram_path

def get_histogram_path(dataset_name,attribute):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    dataset_histogram_attribute_label = histogram_label_template % (dataset_name, attribute)
    dataset_histogram_attribute_path = get_property_value(dataset_conf_path,dataset_histogram_attribute_label)
    return dataset_histogram_attribute_path

def get_mturk_annotated_path(dataset_name,is_pilot_study,batch_number):
    study_label=""
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    if is_pilot_study:
        study_label="pilot_study"
    else:
        study_label="main_study"
    label = annotated_label_template % (dataset_name, study_label, batch_number)
    return get_property_value(dataset_conf_path,label)

def get_english_wikipedia_clikcstream_path(year,month):
    if year> 2017 or year < 2015:
        print ("year should be between 2015 and 2017")
    dataset_conf_path=get_dataset_conf_path("wikipedia")
    path_english_wikipedia_clickstream= get_property_value(dataset_conf_path,clickstream_label)%(year,month)
    return path_english_wikipedia_clickstream

def get_path_inconsistency(dataset_name):
    dataset_conf_path = get_dataset_conf_path(dataset_name)
    inconsistency_label= inconsistency_label_template%dataset_name
    patth_iconsistency= get_property_value(dataset_conf_path,inconsistency_label)
    return patth_iconsistency

def get_path_log(dataset_name):
    path_dataset_conf = get_dataset_conf_path(dataset_name)
    label_log=label_log_template%dataset_name
    return get_property_value(path_dataset_conf,label_log)


def get_path_log_analysis(dataset_name):
    path_dataset_conf = get_dataset_conf_path(dataset_name)
    label_log_anlaysis=label_log_analysis_template%dataset_name
    return get_property_value(path_dataset_conf,label_log_anlaysis)

def get_path_log_quality_checks(dataset_name):
    path_dataset_conf = get_dataset_conf_path(dataset_name)
    label_log_quality_checks=label_log_quality_checks_template%dataset_name
    return get_property_value(path_dataset_conf,label_log_quality_checks)

def get_path_log_low_quality(dataset_name):
    path_dataset_conf = get_dataset_conf_path(dataset_name)
    label_log_low_quality=label_log_low_quality_template%dataset_name
    return get_property_value(path_dataset_conf,label_log_low_quality   )


def get_path_analysis(dataset_name,analysis):
    path_dataset_conf = get_dataset_conf_path(dataset_name)
    label_analysis=annotator_study_label_analysis%(dataset_name,analysis)
    return get_property_value(path_dataset_conf,label_analysis)


def get_path_batches(dataset_name):
    path_dataset_conf = get_dataset_conf_path(dataset_name)
    label_batches=label_batches_template%dataset_name
    return get_property_value(path_dataset_conf,label_batches)

def get_path_experiment_part(experiment,split,part):
    path_dataset_conf = get_dataset_conf_path(experiment)
    path_experiment_part=get_property_value(path_dataset_conf,f"{part}-{split}")
    return path_experiment_part

def get_path_experiment_results(experiment):
    path_dataset_conf = get_dataset_conf_path(experiment)
    path_experiment_results = get_property_value(path_dataset_conf,label_experiment_results)
    return path_experiment_results

def get_path_model(experiment,model):
    path_dataset_conf = get_dataset_conf_path(experiment)
    path_model=get_property_value(path_dataset_conf,f"model-{model}")
    return path_model
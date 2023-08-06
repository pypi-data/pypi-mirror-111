from simpletransformers.classification import ClassificationModel
import pandas as pd
from conf.configuration import *
from sklearn.metrics import *



path_ground_truth= get_path_part('question-categories','ground-truth')
df_ground_truth = pd.read_csv(path_ground_truth,sep="\t",encoding="utf-8")
df_ground_truth.rename(columns={'question':'text','annotation':'labels'},inplace=True)

train_args={'reprocess_input_data': True, 'overwrite_output_dir': True,'num_train_epochs': 1}

model = ClassificationModel(
    "bert", "DeepPavlov/rubert-base-cased", use_cuda=False,num_labels=4
)

df_test = df_ground_truth.sample(frac=0.25)
df_training = df_ground_truth[~df_ground_truth.index.isin(df_test.index)]
model.train_model(df_training)
test_questions = df_test['text'].values
true_labels  = df_test['labels'].values
predicted_labels, outputs = model.predict(test_questions)
f1=f1_score(true_labels,predicted_labels,average='macro')
p=precision_score(true_labels,predicted_labels,average='macro')
r=recall_score(true_labels,predicted_labels,average='macro')

print(f"f1 {f1:2.2}, precision {p:2.2}, recall {r:2.2}")
from annotation.pilot_question_categories import *

def generate_training_examples(study,is_production=True):
    df_training_source=load_subdatset(study,'training-source')
    df_training=load_subdatset(study,'training')
    df_left = df_training_source[~df_training_source.index.isin(df_training.index)]
    examples=[]
    topic = df_training_source.iloc[0,df_training_source.columns.get_loc('topic')]
    topic_id = df_training_source.iloc[0,df_training_source.columns.get_loc('topic-id')]

    counter=0

    indices=[random.randint(100000,100100) for i in range(1,75)]
    for annotation in range(0,5):
        example=df_left[df_left['annotation']==annotation]
        if example.shape[0] !=0:

            examples.append(example.sample(n=1).reset_index())
        else:
            next_index=indices[counter]
            df_example=pd.DataFrame({'task-id':1,'topic':[topic],'topic-id':topic_id,'question-id':[next_index],'question':["To-Add"],'annotation':annotation})

            examples.append(df_example)
            counter = counter + 1
    df_examples=pd.concat(examples)
    df_examples.set_index('question-id',inplace=True)
    save_subdataset(study,'training-examples-to-add',df_examples,check_existence=is_production)


def get_hints():
    hints = {}
    hints[0]= 'Ответ на вопрос – это уникальный факт, с которым согласно большинство людей.'
    hints[1]= 'Ответ на вопрос – инструкция или описание метода для достижения цели/решения задачи.'
    hints[2]= 'Ответ на вопрос – аргументы в пользу или против позиции, принятия решения или совершения действия. С большой вероятностью мнения людей по вопросу расходятся.'
    hints[3]= 'Ответ на вопрос – субъективное мнение/впечатление/эмоция.'
    hints[4]= 'Несерьезный, непонятный или тривиальный вопрос, не относящийся к одной из вышеописанных категорий.'
    return hints

def add_hints(df_training):
    def get_hint(annotation):
        if annotation in range(0,5):
            return df_hints[annotation]
        else:
            return "a hint"
    df_hints=get_hints()
    df_training['hint']=df_training.apply(lambda x:get_hint(x['annotation']),axis=1)


    return df_training

def save_batch_with_toloka_columns(df_batch,path_batch):
    df_batch = df_batch[['question','question-id','task-id','annotation','example-fact', \
                         'example-method','example-opinion','example-argument','example-others','hint']].rename(
        columns={'question-id':"INPUT:id",'task-id':"INPUT:task-id","question":"INPUT:question","annotation":"GOLDEN:category"
            ,"example-fact":"INPUT:example-fact","example-method":"INPUT:example-method","example-opinion":"INPUT:example-opinion",
                 'example-argument':"INPUT:example-argument", "example-others":"INPUT:example-others","hint":"HINT:text"
                 })

    df_batch['GOLDEN:category']=df_batch['GOLDEN:category'].fillna(0).astype(int)
    df_batch['GOLDEN:category']=df_batch['GOLDEN:category'].astype(int)
    df_batch['INPUT:task-id']=df_batch['INPUT:task-id'].fillna(-1).astype(int)

    df_batch.to_csv(path_or_buf=path_batch,sep="\t",encoding="utf-8",columns=['INPUT:id','INPUT:question','INPUT:example-fact','INPUT:example-method','INPUT:example-argument','INPUT:example-opinion','INPUT:example-others',"INPUT:task-id",'GOLDEN:category',"HINT:text"],index=False)

def prepare_training_set(study,is_production=True):
    generate_training_examples(study,is_production)
    df_training=load_subdatset(study,'training')
    df_training['task-page-id']=1
    df_training['task-id']=range(1,df_training.shape[0]+1)
    save_subdataset(study,'training-split',df_training,check_existence=is_production)
    add_examples(study,'training',False)
    df_training=load_subdatset(study,'training-examples',index_col=None)

    df_training=add_hints(df_training)


    path_training_formatted=get_path_part(study,'training-formatted')
    save_batch_with_toloka_columns(df_training,path_training_formatted)

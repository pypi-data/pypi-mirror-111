#sudo docker run  -it -v /mnt/nfs/webis20:/mnt/nfs/webis20 -v /home/befi8957/subjective-questions-taxonomy:/home/host/subjective-questions-taxonomy yamenajjour/questions-taxonomy:4.0  /home/host/subjective-questions-taxonomy/run_topic_identification_experiments.sh
import sys
sys.path.insert(0,"/home/yamenajjour/IdeaProjects/subjective-questions-taxonomy/")
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace,col
from pyspark.sql.types import *
import pandas as pd
from conf.configuration import *
import json
yandex_questions_controversial_topics_path = get_sampled_controversial_path('yandex',3)
yandex_questions_controversial_topics_path_local = get_sampled_controversial_path('yandex',4)

spark = SparkSession.builder.appName('sub-ques-tax1').config('master','yarn').getOrCreate()
yandex_question_controversial_topics_sampled=spark.sparkContext.textFile(yandex_questions_controversial_topics_path)
items=yandex_question_controversial_topics_sampled.map(lambda l : json.loads(l)).collect()
phrases,questions =zip(*items)
questions_sampled = pd.DataFrame({"phrase-id":phrases,"question":questions})
questions_sampled.to_csv(yandex_questions_controversial_topics_path_local,sep="|",encoding="utf-8")
# _*_ coding=utf-8 _*_
import os
import codecs
import sys
from operator import add

from pyspark.sql import SparkSession

import fire

def corpus_word_count(spark,corpus_dir):
	text = ''
	files = [os.path.join(corpus_dir,file) for file in os.listdir(corpus_dir) if file.endswith('txt')]
	for file in files:
		with codecs.open(file,'r',encoding='utf-8') as f:
			text = text+f.read()
			f.close()
	with codecs.open(os.path.join(corpus_dir,'corpus.txt'),'w',encoding='utf-8') as f:
			f.write(text)
			f.close()
	lines = spark.read.text(os.path.join(corpus_dir,'corpus.txt')).rdd.map(lambda r: r[0])
	counts = lines.flatMap(lambda x: x.split(' ')) \
				  .map(lambda x: (x, 1)) \
				  .reduceByKey(add)
	output = counts.collect()
	with codecs.open(os.path.join(corpus_dir,'word_count.txt'),'w',encoding='utf-8') as f:
		for (word, count) in output:
			f.write(word+' '+str(count)+'\n')
		f.close()
		
def process(corpus_dir):
	corpus_dir = os.path.abspath(corpus_dir)
	spark = SparkSession\
	.builder\
	.appName("PythonWordCount")\
	.getOrCreate()
	corpus_word_count(spark,corpus_dir)
	spark.stop()
	
if __name__ == "__main__":
	fire.Fire(process)
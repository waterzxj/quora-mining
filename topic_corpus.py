# _*_ coding=utf-8 _*_
import os
import codecs
import re
from quora import Topic,Question


def get_topic_feed_corpus(topic_name,dir='./corpus'):
	dir = os.path.abspath(dir)
	topic_dir = os.path.join(dir,topic_name)
	if not os.path.exists(topic_dir):
		os.mkdir(topic_dir)
	topic = Topic(topic_name)
	topic_json = topic.get_topic_json()
	feed_questions = topic_json['feed_questions']
	feed_questions_name = [question['question_link'][1:].encode('utf-8') for question in feed_questions]
	for feed_question in feed_questions_name:
		q = Question(feed_question)
		q_json = q.get_question_json()
		answers = q_json['answer']
		corpus = ''
		for a in answers:
			corpus = corpus+'\n'+a['answer_text']
		with codecs.open(os.path.join(topic_dir,re.sub('[\?<>\*\|\:\\\/]','',feed_question).decode('utf-8')+'.txt'),'w',encoding='utf-8') as f:
			f.write(corpus)
			f.close()
		
if __name__ == '__main__':
	#get_topic_feed_corpus('china')
	#get_topic_feed_corpus('taiwan')
	#get_topic_feed_corpus('japan')
	get_topic_feed_corpus('South-Korea')
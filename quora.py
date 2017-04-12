# _*_ coding=utf-8 _*_
import re
import requests
from bs4 import BeautifulSoup

class Topic(object):
	def __init__(self,topic_name):
		self.topic_name = topic_name
		self.url = 'https://www.quora.com/topic/'+self.topic_name
		self.res = requests.get(self.url)
		if self.res.status_code == 200:
			self.soup = BeautifulSoup(self.res.content,'lxml')   
		self.feed_questions = []
		self.Questions = {}
		self.Followers = {}
		self.Edits = {}
		self.related_topics = []
		for a in self.soup.find_all('a',attrs={'class':'question_link'}):
			self.feed_questions.append({'question_link':a['href'],'question_text':a.text})
		Questions_soup = self.soup.find_all('a',attrs={'class':'StatsRow TopicQuestionsStatsRow'})[0]
		self.Questions['Questions_link'] = Questions_soup['href']
		self.Questions['Questions_text'] = Questions_soup.text
		Followers_soup = self.soup.find_all('a',attrs={'class':'StatsRow TopicQuestionsStatsRow'})[0]
		self.Followers['Followers_link'] = Followers_soup['href']
		self.Followers['Followers_text'] = Followers_soup.text
		Edits_soup = self.soup.find_all('a',attrs={'class':'StatsRow TopicQuestionsStatsRow'})[0]
		self.Edits['Edits_link'] = Edits_soup['href']
		self.Edits['Edits_text'] = Edits_soup.text
		for a in self.soup.find_all('a',attrs={'class':'RelatedTopicsListItem HoverMenu'}):
			self.related_topics.append({'topic_link':a['href'],'TopicName':a.find_all('span',attrs={'class':'TopicName'})[0].text})
		self.topic_json = {}
		
	def get_topic_json(self):
		self.topic_json['topic_name'] = self.topic_name
		self.topic_json['topic_url'] = self.url
		self.topic_json['feed_questions'] = self.feed_questions
		self.topic_json['TopicWikiText'] = self.soup.find_all('div',attrs={'class':'TopicWikiText'})[0].text
		self.topic_json['Questions'] = self.Questions
		self.topic_json['Followers'] = self.Followers
		self.topic_json['Edits'] = self.Edits
		self.topic_json['related_topics'] = self.related_topics
		return self.topic_json
		
class Question(object):
	def __init__(self,questoin_name):
		self.questoin_name = questoin_name
		self.url = 'https://www.quora.com/'+self.questoin_name
		self.res = requests.get(self.url)
		if self.res.status_code == 200:
			self.soup = BeautifulSoup(self.res.content,'lxml')
		self.QuestionTopic = []
		for a in self.soup.find_all('a',attrs={'class':'TopicNameLink HoverMenu topic_name'}):
			self.QuestionTopic.append({'topic_link':a['href'],'TopicName':a.text})
		self.answer_count = int(re.findall('[0-9]+',self.soup.find_all('div',attrs={'class':'answer_count'})[0].text)[0])
		#self.answer_count = int(self.soup.find_all('div',attrs={'class':'answer_count'})[0].text.split(' ')[0])
		self.answer = []
		for d1 in self.soup.find_all('div',attrs={'class':'AnswerBase'}):
			for d2 in d1.find_all('div',attrs={'class':'AnswerHeader ContentHeader'}):
				user = {}
				for a in d2.find_all('a',attrs={'class':'user'}):
					user['user_link'] = a['href']
					user['UserName'] = a.text
			self.answer.append({'user':user,'answer_text':d1.find_all('span',attrs={'class':'rendered_qtext'})[0].text})
		self.question_json = {}
		
	def get_question_json(self):
		self.question_json['questoin_name'] = self.questoin_name
		self.question_json['url'] = self.url
		self.question_json['QuestionTopic'] = self.QuestionTopic
		self.question_json['answer_count'] = self.answer_count
		self.question_json['answer'] = self.answer
		return self.question_json
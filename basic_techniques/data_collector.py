import datetime
import re
import time
from twitterscraper import query_tweets
import json

'''
-Object that uses twitterscraper to scrape twitter for a targeted selection of tweets
-Also:
	-cleans the data using several regex patterns (remove urls, hashtags, handles, and all punctuation)
	-encodes the text in utf-8
	-removes unnecessary/additional spaces
	-removes newline characters (\n)
	-makes everything lowercase

FUTURE:
	-We need to be able to collect data and store it somewhere...
		-DB?
		-txt file?
		-???
	-With more complete and permanent collection of data comes new issues:
		-how do we avoid collecting the same data twice, but also avoid unintentional biasing?
			-ie. it's not enough to just check to see if a certain word/sentence already appears in our current dataset
			 because it is totally possible that the same word/sentence has been written more than once and should be 
			 represented as such
'''

class DataCollector(object):

	def __init__(self):
		self.corpus = []
		self.idtotweet = {}
		self.load_corpus()

	'''
	In the future, this method should allow more complex queries if necessary and provide a
	more complete wrapper of the query_tweets API
	'''
	def collect_data(self):
		start_time = time.time()
		print("INFO: starting to gather tweets...")
		list_of_tweets = query_tweets(query='', limit=40000, begindate=datetime.date(2017,2,1), lang='en') #get list of tweets from twitterscraper API
		print("INFO: -----TOTAL AMOUNT OF TWEETS: {length}-----".format(length=len(list_of_tweets)))
		print("INFO: execution time for gathering of tweets: {time} seconds".format(time=time.time() - start_time))
		print('')

		ount = 0

		print('INFO: *****ADDING NEW TWEETS*****')
		for tweet in list_of_tweets:
			if tweet.id not in self.idtotweet:
				self.idtotweet[tweet.id] = tweet.text
				count += 1

		print('INFO: {cnt} new tweets added to the corpus!'.format(cnt=count))

		with open('read_from.json', 'w') as fw:
			json.dump(self.idtotweet, fw)

		for key in self.idtotweet:
			self.corpus.append(idtotweet[key])

		print('INFO: new length of permanent corpus: {twts}'.format(twts=len(idtotweet)))

	def load_corpus(self):
		tweet_file = open('read_from.json')
		tweet_str = tweet_file.read()
		tweet_file.close()

		print('INFO: starting to load json file...')
		loaded_tweets = json.loads(tweet_str)
		print('INFO: json file successfully loaded!\n')

		for key in loaded_tweets:
			tw_data = loaded_tweets[key].encode('utf-8')
			tw_id = key.encode('utf-8')

			self.idtotweet[tw_id] = tw_data

		for key in self.idtotweet:
			self.corpus.append(self.idtotweet[key])

	def clean_corpus(self):
		for i, sentence in enumerate(self.corpus):
			#sentence = sentence.encode('utf-8')
			self.corpus[i] = sentence.lower()
		self.remove_urls()
		self.remove_hashtags()
		self.remove_handles()
		self.remove_punctuation()
		self.remove_extra_whitespace()

	def remove_urls(self):
		URL_PATTERN = re.compile(r'(?i)((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))', re.IGNORECASE)
		
		for i, sentence in enumerate(self.corpus):
			self.corpus[i] = URL_PATTERN.sub('', sentence)

	def remove_hashtags(self):
		HASHTAG_PATTERN = re.compile(r'#(.*?)[\s]', re.IGNORECASE)

		for i, sentence in enumerate(self.corpus):
			self.corpus[i] = HASHTAG_PATTERN.sub('', sentence)

	def remove_handles(self):
		HANDLE_PATTERN = re.compile(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', re.IGNORECASE)

		for i, sentence in enumerate(self.corpus):
			self.corpus[i] = HANDLE_PATTERN.sub('', sentence)

	def remove_punctuation(self):
		PUNCTUATION_PATTERN = re.compile(r'[^a-zA-Z\s]', re.IGNORECASE)

		for i, sentence in enumerate(self.corpus):
			sentence = PUNCTUATION_PATTERN.sub('', sentence)
			sentence = re.sub(' +', ' ', sentence)
			self.corpus[i] = sentence.replace('\n', '')

	def remove_extra_whitespace(self):
		for i, sentence in enumerate(self.corpus):
			sentence = sentence.lstrip()
			self.corpus[i] = ' '.join(sentence.split())

	
import datetime
import re
import time
from twitterscraper import query_tweets
from basic_language_model import *

'''
-Script that uses twitterscraper to scrape twitter for a targeted selection of tweets
	-cleans the data using several regex patterns (remove urls, hashtags, handles, and all punctuation)
	-encodes the text in utf-8
	-removes unnecessary/additional spaces
	-removes newline characters (\n)
	-makes everything lowercase
'''

if __name__ == '__main__':

	'''keep track of when execution started'''
	start_time = time.time()

	'''defines regex patterns in order to clean the tweets, need to:
		-remove URLs
		-remove hashtags
		-remove handles
		-remove punctuation
	'''
	URL_PATTERN = re.compile(r'(?i)((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))', re.IGNORECASE)
	HASHTAG_PATTERN = re.compile(r'#(.*?)[\s]', re.IGNORECASE)
	HANDLE_PATTERN = re.compile(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', re.IGNORECASE)
	PUNCTUATION_PATTERN = re.compile(r'[^a-zA-Z\s]', re.IGNORECASE)

	list_of_tweets = query_tweets(query="", limit=40, begindate=datetime.date(2018, 1, 1), lang='en') #get list of tweets from twitterscraper API
	clean_tweets = []

	print(len(list_of_tweets))

	for tweet in list_of_tweets:
		'''iterate through the tweets we found, encode to utf-8 (python string standard), and remove any regex pattern matches'''
		clean = tweet.text.encode('utf-8')
		clean = URL_PATTERN.sub('', clean)
		clean = HASHTAG_PATTERN.sub('', clean)
		clean = HANDLE_PATTERN.sub('', clean)
		clean = PUNCTUATION_PATTERN.sub('', clean)
		clean = re.sub(' +',' ', clean)
		clean = clean.replace('\n', '')

		'''add the new cleaned tweet to the list of clean_tweets'''
		clean_tweets.append(clean.lower())


	'''print the resulting tweets'''
	print(clean_tweets)

	'''clean_tweets now acting as the corpus of our data'''
	print(assign_probability('go', clean_tweets)) #what is the probability that any word in the corpus was 'go'?

	print(get_unique_tokens_count(clean_tweets)) #get a count of every unique word in the corpus


	'''print the length of execution time'''
	print("--- %s seconds" % (time.time() - start_time))


'''
NEXT STEPS:
-How do we assign probabilities to words? -> somewhat done
-How do we make predictions?
ACTUALLY need to build the language model now
-Structure/organize/clean this code
'''
	
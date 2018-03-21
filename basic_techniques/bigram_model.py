from data_collector import DataCollector
from basic_utils import get_tokens
import operator


class BigramModel(object):

	def __init__(self, data_collector=DataCollector()):
		self.data_collector = data_collector
		self.bigrams = dict()
		self.get_unique_bigrams()

	def get_unique_bigrams(self):
		#generate unique bigrams from these tokens, assign/calculate their frequency
		#use utils.py to get a list of all tokens in the corupus
		all_tokens = get_tokens(self.data_collector.corpus)

		for i in xrange(len(all_tokens) - 1):
			key = (all_tokens[i], all_tokens[i+1])

			if (self.bigrams.has_key(key)):
				self.bigrams[key] += 1
			else:
				self.bigrams[key] = 1

		#sort the bigrams from most frequent to least frequent
		self.bigrams=sorted(self.bigrams.items(), key=operator.itemgetter(1), reverse=True)


	'''
	bigram is a list in the format
	[((word_one, word_two), freqency_of_bigram), ...], ie. [((bigram), frequency_of_bigram), ...]
	-this function prints the first word it was given, and then searches for the most frequent bigram in the list
	where 'word' is the first element of the bigram. word then becomes the second element of that bigram and the 
	loop begins again

	if word is not in the bigram list at all...loop breaks and the sentence terminates early :(
	'''
	def get_bigram_sentence(self, word, n=20):
		for i in xrange(n):
			print word,
			word = next((element[0][1] for element in self.bigrams if element[0][0] == word), None)
			if not word:
				break	


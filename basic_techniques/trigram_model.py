from data_collector import DataCollector
from basic_utils import get_tokens
import operator


class TrigramModel(object):

	def __init__(self, data_collector=None):
		if data_collector is None:
			data_collector = DataCollector()
		else:
			self.data_collector = data_collector
		self.trigrams = dict()
		self.get_unique_trigrams()

	def get_unique_trigrams(self):
		#generate unique trigrams from these tokens, assign/calculate their frequency
		#use utils.py to get a list of all tokens in the corupus
		all_tokens = get_tokens(self.data_collector.corpus)

		for i in xrange(len(all_tokens) - 2):
			key = (all_tokens[i], all_tokens[i+1], all_tokens[i+2])

			if (self.trigrams.has_key(key)):
				self.trigrams[key] += 1
			else:
				self.trigrams[key] = 1

		#sort the trigrams from most frequent to least frequent
		self.trigrams=sorted(self.trigrams.items(), key=operator.itemgetter(1), reverse=True)

		'''
		x = 0
		while (x < 40):
			print(self.trigrams[x])
			x += 1
		'''

	'''
	bigram is a list in the format
	[((word_one, word_two), freqency_of_bigram), ...], ie. [((bigram), frequency_of_bigram), ...]
	-this function prints the first word it was given, and then searches for the most frequent bigram in the list
	where 'word' is the first element of the bigram. word then becomes the second element of that bigram and the 
	loop begins again
	if word is not in the bigram list at all...loop breaks and the sentence terminates early :(
	'''
	def get_trigram_sentence(self, word1, word2, n=20):
		sentence = [word1, word2]
		for i in xrange(n-2):
			new_word = next((element[0][2] for element in self.trigrams if element[0][0] == word1 and element[0][1] == word2), None)
			sentence.append(new_word)
			word1, word2 = word2, new_word
			if not word1 or not word2:
				print('WARNING: no more trigrams available...exiting.')
				break

		return " ".join(sentence)


#collect data/clean it
collector = DataCollector()
collector.clean_corpus()
#print(collector.corpus)

trigram_model = TrigramModel(collector)





#start with a word and generate a sentence based on bigrams
start_word1 = 'i'
start_word2 = 'am'

print('start word: {w1} {w2}'.format(w1=start_word1, w2=start_word2))

print('3-gram sentence: \"{sent}\"'.format(sent=trigram_model.get_trigram_sentence(start_word1, start_word2, 5)))
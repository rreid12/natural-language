import os
from data_collector import DataCollector
from basic_utils import get_tokens, get_unique_tokens_count
import operator


class BigramModel(object):

	def __init__(self, data_collector=None):
		if data_collector is None:
			data_collector = DataCollector()
		else:
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
	def get_bigram_sentence(self, word, lengths, n=20):
		word_idx = 0
		sentence = []
		for i in range(n):
			if i < n -1:
				word_idx += 1
			sentence.append(word)
			word = next((element[0][1] for element in self.bigrams if element[0][0] == word and len(element[0][1]) == int(lengths[word_idx])), None)
			if not word and i < n - 1:
				print('DEBUG: n value: {n}'.format(n=n))
				print('DEBUG: i value: {i}'.format(i=i))
				print('DEBUG: current word: {word}'.format(word=word))
				print('WARNING: terminated early because no more matching bigrams were found for this seed...')
				return " ".join(sentence)

		return " ".join(sentence)

	def get_best_seed_word(self, length):
		tokens = get_unique_tokens_count(self.data_collector.corpus)

		for tkn in tokens:
			if(len(tkn[0]) == int(length)):
				return tkn[0]

	#maybe?			
	'''
	def get_possible_seed_words(self, length):
		all_tokens = get_unique_tokens_count(self.data_collector.corpus)

		possible_seeds = []

		for tkn in all_tokens:
			if (len(tkn[0]) == int(length)):
				possible_seeds.append(tkn[0])

		return possible_seeds'''


#collect data/clean it
collector = DataCollector()
collector.clean_corpus()
#print(collector.corpus)

bigram_model = BigramModel(collector)



dir_name = 'txt_examples'

for filename in os.listdir(dir_name):
	print('INFO: generating text for {fname}'.format(fname=filename))
	word_lengths = []
	f = open('{directory}/{file}'.format(directory=dir_name, file=filename), 'r')

	for line in f:
		word_lengths.append(line.replace('\n', ''))

	#start with a word and generate a sentence based on bigrams
	start_word = bigram_model.get_best_seed_word(word_lengths[0])

	print("INFO: start_word: %s " % start_word)
	print("INFO: 2-gram sentence: \" {sent} \"".format(sent=bigram_model.get_bigram_sentence(start_word, word_lengths, len(word_lengths))))
	print('')



#maybe?
'''
pos_seeds = bigram_model.get_possible_seed_words(word_lengths[0])
print('INFO: ----Possible seeds found: {seeds}-----'.format(seeds=len(pos_seeds)))

sentences = []

for seed in pos_seeds:
	sent = bigram_model.get_bigram_sentence(seed, word_lengths, len(word_lengths))
	if (sent != None):
		sentences.append(sent)

print(sentences)
print('INFO: -----# of sentences generated: {count}-----'.format(count=len(sentences)))
'''
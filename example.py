from data_collector import DataCollector
from basic_utils import get_tokens
import operator

'''
bigram is a list in the format
[((word_one, word_two), freqency_of_bigram), ...], ie. [((bigram), frequency_of_bigram), ...]
-this function prints the first word it was given, and then searches for the most frequent bigram in the list
where 'word' is the first element of the bigram. word then becomes the second element of that bigram and the 
loop begins again

if word is not in the bigram list at all...loop breaks and the sentence terminates early :(
'''
def get_bigram_sentence(word, n=20):
	for i in xrange(n):
		print word,
		word = next((element[0][1] for element in bigram if element[0][0] == word), None)
		if not word:
			break	


#collect data/clean it
collector = DataCollector()
collector.collect_data()
collector.clean_corpus()
print(collector.corpus)

#use utils.py to get a list of all tokens in the corupus
all_tokens = get_tokens(collector.corpus)

#generate unique bigrams from these tokens, assign/calculate their frequency
bigram = dict()

for i in xrange(len(all_tokens) - 1):
	key = (all_tokens[i], all_tokens[i+1])

	if (bigram.has_key(key)):
		bigram[key] += 1
	else:
		bigram[key] = 1

#sort the bigrams from most frequent to least frequent
bigram = sorted(bigram.items(), key=operator.itemgetter(1), reverse=True)


#start with a word and generate a sentence based on bigrams
start_word = 'i'

print("start_word: %s " % start_word)

print "2-gram sentence: \"", 
get_bigram_sentence(start_word, 3)
print "\""
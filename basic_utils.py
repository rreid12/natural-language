import os
from decimal import *
import operator
from nltk import ngrams


'''
Get the number of tokens in the corpus
'''
def count_tokens(corpus):
	count = 0

	for sent in corpus:
		count += len(sent.split())

	return count

'''
Get a count of all the unique tokens in the corpus
'''
def get_unique_tokens_count(corpus):
	unique_tokens_count = {}
	tokens = get_tokens(corpus)

	for tkn in tokens:
		if tkn not in unique_tokens_count:
			unique_tokens_count[tkn] = 1
		else:
			unique_tokens_count[tkn] += 1

	#returns a *sorted(greatest to least)* list of tuples in the format (WORD, # OF OCCURENCES)
	return sorted(unique_tokens_count.items(), key=operator.itemgetter(1), reverse=True)

'''
Get a list of all unique tokens in the corpus
'''
def get_unique_tokens(corpus):
	unique_tokens = []
	tokens = get_tokens(corpus)

	for tkn in tokens:
		if tkn not in unique_tokens:
			unique_tokens.append(tkn)

	return unique_tokens


'''
Get a list of all tokens in the corpus
'''
def get_tokens(corpus):
	tokens = []

	for sent in corpus:
		tokens += sent.split(" ")

	return tokens

'''
Assign a probability to a specified word in the corpus (decimal # in the range of 0 to 1)
'''
def assign_probability(word, corpus):
	count = 0

	tokens = get_tokens(corpus)

	for tkn in tokens:
		if (tkn == word):
			#print(tkn)
			count += 1

	total_words = count_tokens(corpus)
	print('TOTAL WORDS in corpus: {total}'.format(total=total_words))
	print('{word} OCCURRENCES in corpus: {count}'.format(word=word, count=count))
	getcontext().prec = 10 #sets precision to 10 decimal places

	return Decimal(count) / Decimal(total_words) #Decimal is a class that provides super precise numbers for calculations

'''
Gets ngrams based on a sentence and a custom value of n
'''
def get_ngrams(n, sent):
	return ngrams(sent.split(), n)

#testing
if __name__ == '__main__':
	print(count_tokens(['the there they their', 'them they there their']))
	print(assign_probability('the', ['the there they their', 'them they there their']))
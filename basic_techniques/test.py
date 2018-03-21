from data_collector import DataCollector
from bigram_model import BigramModel
from trigram_model import TrigramModel

import re

'''
URL_PATTERN = re.compile(r'(?i)((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))', re.IGNORECASE)
HASHTAG_PATTERN = re.compile(r'#(.*?)[\s]', re.IGNORECASE)
HANDLE_PATTERN = re.compile(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', re.IGNORECASE)
PUNCTUATION_PATTERN = re.compile(r'[^a-zA-Z\s]', re.IGNORECASE)

text = '@carl124 I absolutely hate #tacos! they are ABSOLUTELY disgusting!! just look @ this one: https://www.google.com/search?q=taco&safe=off&client=ubuntu&hs=JWm&channel=fs&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjb4ZDnl_7ZAhXBxFkKHcxsAcoQ_AUICygC&biw=1855&bih=982#imgrc=Van76mzs7lMt_M:'

print(text)

print('INFO: removing URLs...')
text = URL_PATTERN.sub('', text)
print(text)

print('INFO: removing hashtags...')
text = HASHTAG_PATTERN.sub('', text)
print(text)

print('INFO: removing handles...')
text = HANDLE_PATTERN.sub('', text)
print(text)

print('INFO: removing punctuation...')
text = PUNCTUATION_PATTERN.sub('', text)
print(text)

print('INFO: aaaaand lowercase...')
text = text.lower()
print(text)

print('INFO: removing whitespaces...')
text = text.lstrip()
text = ' '.join(text.split())
print(text)'''

#collect data/clean it
collector = DataCollector()
collector.collect_data()
collector.clean_corpus()
print(collector.corpus)

bigram_model = BigramModel(collector)





#start with a word and generate a sentence based on bigrams
start_word = 'i'

print("start_word: %s " % start_word)

print "2-gram sentence: \"", 
bigram_model.get_bigram_sentence(start_word, 3)
print "\""

trigram_model = TrigramModel(collector)

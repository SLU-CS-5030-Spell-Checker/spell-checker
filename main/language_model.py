import re
import collections
import itertools
from itertools import product
from functools import cmp_to_key

def words(text):
    """filter body of text for words"""
    return re.findall('[a-z]+', text.lower())

def train(text, model=None):
    """generate or update a word model (dictionary of word:frequency)"""
    model = collections.defaultdict(lambda: 0) if model is None else model
    for word in words(text):
        model[word] += 1
    return model

def train_from_files(file_list, model=None):
    for f in file_list:
        model = train(open(f).read(), model)
    return model


word_model = train(open(r'C:\Users\jca26\OneDrive\Documents\csci_5030\bible.txt').read())
real_words = set(word_model)

# add other texts here, they are used to train the word frequency model
texts = [
    r'C:\Users\jca26\OneDrive\Documents\csci_5030\shakespeare.txt',
    r'C:\Users\jca26\OneDrive\Documents\csci_5030\sherlockholmes.txt',
    r'C:\Users\jca26\OneDrive\Documents\csci_5030\lemmas.txt',
    ]
# enhance the model with real bodies of english so we know which words are more common than others
word_model = train_from_files(texts, word_model)
##real_words = set(word_model)

print('Total Word Set: ', len(word_model))
print('Model Precision: %s' % (float(sum(word_model.values()))/len(word_model)))

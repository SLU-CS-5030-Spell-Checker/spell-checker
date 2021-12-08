import re
from collections import Counter
from heapq import nlargest
import pickle

def words(text): return re.findall(r'\w+', text.lower())
t1 = open('bible.txt').read()
WORDS = Counter(words(t1))

def totalProb(words, word): 
    #lang model
    if len(words.split())==2:
        f = open(r'multiwordfreq_n3_irish', 'rb')
    else:
        f = open(r'multiwordfreq_n2_irish', 'rb')
    new_dict = pickle.load(f)
    f.close()
    w = tuple(words.split())
    options = new_dict.get(w)
    if options == None:
        freq = 0
    else:
        freq = options.get(word)
        if freq == None:
            freq = 0
    N=sum(WORDS.values())
    M =len(new_dict)
    freq = freq/M
    return ((1/8)*WORDS[word] / N + (7/8)*freq)

def oneEditDist(word):
    letters    = 'abcdefghijklmnopqrstuvwxyzáéíóú'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def twoEditDist(word): 
    return (e2 for e1 in oneEditDist(word) for e2 in oneEditDist(e1))

def wordFilter(words): 
    return set(w for w in words if w in WORDS)

def possible(word): 
    ans = wordFilter(oneEditDist(word))
    ans.update(wordFilter(twoEditDist(word)))
    return ans

def correction(words, word): 
    d = {}
    if word in WORDS:
        return [word]
    for w in possible(word):
        if word[0].isupper():
            d[w.capitalize()] = totalProb(words, w)
        else:
            d[w] = totalProb(words, w)
    return nlargest(3,d, key=d.get)


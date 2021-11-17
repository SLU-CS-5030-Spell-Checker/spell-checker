import re

file = open('shakespeare.txt').read()  #placeholder until we find a better corpus
justwords = re.findall(r'\w+', file.lower())
letters = 'abcdefghijklmnopqrstuvwxyz'

#create a list of every possible word that is one edit distance away
def oneEditDist(word, alpha):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in alpha]
    inserts    = [L + c + R               for L, R in splits for c in alpha]
    return list(deletes + transposes + replaces + inserts)

#create a list of every possible word that is two edit distance away
def twoEditDist(word, alpha):
    return list(e2 for e1 in oneEditDist(word, alpha) for e2 in oneEditDist(e1, alpha))

#filter a list of words for words found in corpus
def wordFilter(words):
    truewords = []
    for w in words:
        if w in justwords:
            truewords.append(w)
    return truewords

#return the frequency of the word in the corpus
def P(word): 
    #total = len(justwords)
    pword = justwords.count(word)
    #return pword/total
    return pword

#creates and sorts a word list by frequency
def correction(word): 
    words = wordFilter(oneEditDist(word, letters))  #only considers oneEdit
    pc = []
    for w in words:
        pc.append(P(w))
    d = sorted(dict(zip(words,pc)))
    return d

print(correction('helo'))


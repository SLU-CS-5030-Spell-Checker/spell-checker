import pickle
from django.http.response import JsonResponse
import requests 
import json
from django.shortcuts import render
from urllib.parse import parse_qs, urlparse
import re

##file = open(r'C:\Users\jca26\OneDrive\Documents\csci_5030\shakespeare.txt').read()
##justwords = re.findall(r'\w+', file.lower())

#returns frequency of word in corpus
def errormodel(word):
    f = open(r'C:\Users\jca26\OneDrive\Documents\csci_5030\singlewordfreq.txt','rb')
    allwords = pickle.load(f)
    f.close()
    for i in allwords:
        if i[1] == word:
            return i[0]
    return 0

#returns frequency of word given previous word (Ngram)
def langmodel(words, word):
    try:
        if len(words.split())==2:  #loads in different file depending on n
            f = open(r'C:\Users\jca26\OneDrive\Documents\csci_5030\multiwordfreq_n2.txt','rb')
        else:
            f = open(r'C:\Users\jca26\OneDrive\Documents\csci_5030\multiwordfreq_n3.txt','rb')
        new_dict = pickle.load(f)
        f.close()
        w = tuple(words.split())
        options = new_dict.get(w)
        freq = options.get(word)
        if freq == None:
            freq=0.1
        return freq
    except:
        return 0.1

#determines final probability by combining errormodel and langmodel
def totalprob(words, word):
    return (errormodel(word)*langmodel(words,word))


#creates list of eligiable words one edit dist apart
def oneEditDist(word):
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in alpha]
    inserts    = [L + c + R               for L, R in splits for c in alpha]
    return list(deletes + transposes + replaces + inserts)

#creates list of eligiable words two edit dist apart
def twoEditDist(word):
    return list(e2 for e1 in oneEditDist(word) for e2 in oneEditDist(e1))

#returns the list of one edit dist (can be both but it is slow)
def possible(word):
    return oneEditDist(word)

#filters a list of words compared to the corpus
def wordFilter(words):
    f = open(r'C:\Users\jca26\OneDrive\Documents\csci_5030\singlewordfreq.txt','rb')
    allwords = pickle.load(f)
    f.close()
    real = []
    for w in words:
        for i in allwords:
            if i[1] == w:
                real.append(w)
    return real

#sorts list of words by total probability
def correction(words):
    word = words.split()[-1]
    words = ' '.join(words.split()[:-1])
    print(word)
    print(words)
    true = wordFilter(possible(word))
    pc = []
    for w in true:
        pc.append(totalprob(words,w))
    d = dict(zip(true,pc))
    marklist=sorted((value, key) for (key,value) in d.items())
    sortdict=dict([(k,v) for v,k in marklist])
    bestwords = (list(sortdict.keys()))
    bestwords.reverse()
    return bestwords


##print(correction(words,word))

## render views function
def index(request):
    return render(request,"main/index.html")

## spell check function
def spell_check(request):
    word_text=request.GET.get('word')
    print(word_text)## for testing in console
    word_string= json.dumps(word_text)
    print(word_string)## for testing in console
    replaced_string = word_string.replace('"', "")
    print(replaced_string)## for testing in console
    word_list= correction(replaced_string)
    ##word_list= h.suggest(replaced_string)
    print(word_list)## for testing in console
    data ={'output': word_list}
    print(data)## for testing in console
    return JsonResponse(data)

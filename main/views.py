import pickle
from django.http.response import JsonResponse
import json
from django.shortcuts import render
from urllib.parse import parse_qs, urlparse
import re
import re
from collections import Counter
from heapq import nlargest
import pickle

def words(text): return re.findall(r'\w+', text.lower())
WORDS = Counter(words(open(r'C:\Users\jca26\OneDrive\Documents\csci_5030\bible.txt').read()))
def totalProb(words, word): 
    #lang model
    if len(words.split())==2:
        f = open(r'C:\Users\jca26\OneDrive\Documents\csci_5030\multiwordfreq_n2.txt','rb')
    else:
        f = open(r'C:\Users\jca26\OneDrive\Documents\csci_5030\multiwordfreq_n3.txt','rb')
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
    return (WORDS[word] / N + freq)

def oneEditDist(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
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
    for w in possible(word):
        if word[0].isupper():
            d[w.capitalize()] = totalProb(words, w)
        else:
            d[w] = totalProb(words, w)
    return nlargest(3,d, key=d.get)
    
def index(request):
    return render(request,"main/index.html")

## spell check function
def spell_check(request):
    word_text=request.GET.get('word')
    words=request.GET.get('words')
    word_string= json.dumps(word_text)
    words_string= json.dumps(words)
    replaced_string = word_string.replace('"', "")
    ##replaced_string='prayd'
    ##words_string='the camel'
    word_list= correction(words_string,replaced_string)
    print(word_list)
    data ={'output': word_list}
    return JsonResponse(data)

def spell_check2(request):
    word_input= request.GET.get('word_list')
    word_list= json.loads(word_input)
    misspelled_words=[]
    for i in word_list:
        suggestion= wordFilter([i])
        if not suggestion:
            misspelled_words.append(i)
    data={'output':json.dumps(misspelled_words)}
    return JsonResponse(data)


def get_context_words(word,words):
    num_context_words= 3
    word_index= words.index(word)
    start_context_index= word_index-num_context_words
    if start_context_index<=0:
        start_context_index=0
    context_words=[]
    for x in range(start_context_index,word_index):
        context_words.append(words[x])
    clean_words= clean_context_words(context_words)
    return ' '.join(clean_words)

def clean_context_words(dirty_words):
    for i in range(len(dirty_words)-1,-1,-1):
        suggestion= wordFilter([dirty_words[i]])
        if suggestion:
            continue
        else:
            for j in range(i,-1,-1):
               del dirty_words[j]
            break
    return dirty_words

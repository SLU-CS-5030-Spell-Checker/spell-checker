## Import necessary packages
from django.http.response import JsonResponse
import requests 
import json
from django.shortcuts import render
from urllib.parse import parse_qs, urlparse
from hunspell import Hunspell
import re

import requests
page = requests.get("https://www.gutenberg.org/files/1661/1661-0.txt")
##irish= open(r'C:\Users\jca26\OneDrive\Documents\csci_5030\irish\bible.txt').read()
from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')
text= soup.get_text()

## define hunspell variables
h = Hunspell()

#create a list of all possible words that are one edit distance away
def oneEditDist(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return (deletes + transposes + replaces + inserts)

def isRealWords(words):
    realWordsList = text
    realWords = []
    for w in words:
        if w in realWordsList:
            realWords.append(w)
    return realWords
    

def possibilities(word):
    return isRealWords(oneEditDist(word))

file = open(r'C:\Users\jca26\OneDrive\Documents\csci_5030\shakespeare.txt').read()
justwords = re.findall(r'\w+', file.lower())

def oneEditDist(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return list(deletes + transposes + replaces + inserts)

def twoEditDist(word):
    return list(e2 for e1 in oneEditDist(word) for e2 in oneEditDist(e1))

def wordFilter(words):
    truewords = []
    for w in words:
        if w in justwords:
            truewords.append(w)
    return truewords

def P(word): 
    total = len(justwords)
    pword = justwords.count(word)
    return pword/total
    
def correction(word): 
    words = wordFilter(oneEditDist(word))
    pc = []
    for w in words:
        pc.append(P(w))
    d = sorted(dict(zip(words,pc)))
    return d

## render views function
def index(request):
    return render(request,"main/index.html")

## hunspell check function
def spell_check(request):
    word_text=request.GET.get('word')
    print(word_text)## for testing in console
    word_string= json.dumps(word_text)
    print(word_string)## for testing in console
    replaced_string = word_string.replace('"', "")
    print(replaced_string)## for testing in console
    word_list= correction(replaced_string)
    print(word_list)## for testing in console
    data ={'output': word_list}
    print(data)## for testing in console
    return JsonResponse(data)

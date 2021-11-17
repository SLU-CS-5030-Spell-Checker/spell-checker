from django.http.response import JsonResponse
import requests 
import json
from django.shortcuts import render
from urllib.parse import parse_qs, urlparse
from hunspell import Hunspell
import unicodedata
import io

import requests
page = requests.get("https://www.gutenberg.org/files/1661/1661-0.txt")
from bs4 import BeautifulSoup
##soup = BeautifulSoup(page.content, 'html.parser')
text= io.open(r'C:\Users\jca26\OneDrive\Documents\csci_5030\irish\bible.txt',encoding="UTF-8")
##text= soup.get_text()

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

## render views function
def index(request):
    return render(request,"main/index_irish.html")

## hunspell check function
def spell_check(request):
    word_text=request.GET.get('word')
    print(word_text)## for testing in console
    word_string= json.dumps(word_text)
    print(word_string)## for testing in console
    replaced_string = word_string.replace('"', "")
    print(replaced_string)## for testing in console
    word_list= oneEditDist(replaced_string)
    print(word_list)## for testing in console
    data ={'output': word_list}
    print(data)## for testing in console
    return JsonResponse(data)

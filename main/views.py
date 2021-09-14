from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

## Webscrape gutenberg text files
page = requests.get("https://www.gutenberg.org/files/1661/1661-0.txt")

## Parse the html into text
soup = BeautifulSoup(page.content, 'html.parser')
text= soup.get_text()

#create a list of all possible words that are one edit distance away
def oneEditDist(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return (deletes + transposes + replaces + inserts)

## Return a list of real words from gutenberg text          
def isRealWords(words):
    realWordsList = text
    realWords = []
    for w in words:
        if w in realWordsList:
            realWords.append(w)
    return realWords
    
## Return possible spell corrections
def possibilities(word):
    return isRealWords(oneEditDist(word))

 
# Create your views here.
def index(request):
    ## Get url parameters "enter_text"
    result = request.GET.dict()
    ## If not available start with default parameters
    res = not bool(result)
    if res==True :
        result = {'enter_text': 'default'}
        word_text=(result['enter_text'])
        word_list=possibilities(word_text)
        data ={'output': word_list}
        ## Else enter your word of choice
    else:
        word_text=(result['enter_text'])
        word_list=possibilities(word_text)
        data ={'output': word_list}
    return render(request, "main/index.html",data)



import requests
page = requests.get("https://www.gutenberg.org/files/1661/1661-0.txt")
from bs4 import BeautifulSoup
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

#def twoEditDist(word):
#    twoEdits = []
#    for e1 in oneEditDist(word):
#        for e2 in oneEditDist(e1):
#            twoEdits.append(e2)
#    return twoEdits
            

def isRealWords(words):
    realWordsList = text
    realWords = []
    for w in words:
        if w in realWordsList:
            realWords.append(w)
    return realWords
    

def possibilities(word):
    return isRealWords(oneEditDist(word))

poss_word= ('doj')
word_list=possibilities(poss_word)
print(word_list)
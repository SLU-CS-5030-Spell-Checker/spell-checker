import pickle


#returns frequency of word in corpus
def errormodel(word):
    f = open('singlewordfreq','rb')
    allwords = pickle.load(f)
    f.close()
    for i in allwords:
        if i[1] == word:
            return i[0]
    return 0

#returns frequency of word given previous word (Ngram)
def langmodel(words, word):
    if len(words.split())==2:  #loads in different file depending on n
        f = open('multiwordfreq2','rb')
    else:
        f = open('multiwordfreq3','rb')
    new_dict = pickle.load(f)
    f.close()
    w = tuple(words.split())
    options = new_dict.get(w)
    freq = options.get(word)
    if freq == None:
        freq=0
    return freq

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
    f = open('singlewordfreq','rb')
    allwords = pickle.load(f)
    f.close()
    real = []
    for w in words:
        for i in allwords:
            if i[1] == w:
                real.append(w)
    return real

#sorts list of words by total probability
def correction(words, word): 
    true = wordFilter(possible(word))
    pc = []
    for w in true:
        pc.append(totalprob(words,w))
    d = sorted(dict(zip(true,pc)), reverse = True)
    return d


#example of how to call above functions
#print(correction('blood up','wih'))

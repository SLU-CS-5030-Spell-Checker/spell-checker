import pickle


def totalprob(word, words): 
    #langmodel
    try:
        if len(words.split())==2:  #loads in different file depending on n
            f = open(r'multiwordfreq_irish_n2.txt','rb')
        else:
            f = open(r'multiwordfreq_irish_n3.txt','rb')
        new_dict = pickle.load(f)
        f.close()
        w = tuple(words.split())
        options = new_dict.get(w)
        freq = options.get(word)
        if freq == None:
            freq=0.1
    except:
        freq =  0.1
    #errormodel
    ff = open(r'singlewordfreq_irish.txt','rb')
    allwords = pickle.load(ff)
    ff.close()
    for i in allwords:
    	if i[1]==word:
    		freq2 = i[0]
    	else:
    		freq2 = 0.1
    return freq2 * freq

def oneEditDist(word):
    letters    = 'abcdefghijklmnopqrstuvwxyzáéíóú'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def wordFilter(words):
	f = open(r'singlewordfreq_irish.txt','rb')
	allwords = pickle.load(f)
	return set(w for w in words if w in allwords)

def possible(word): 
    return (wordFilter(oneEditDist(word)))

def correction(words): 
    word = words.split()[-1]
    words = ' '.join(words.split()[:-1])
    cans = possible(word)
    pc = []
    if len(cans)>0:
    	for c in cans:
    		pc.append(totalprob(c,words))
    d = dict(zip(cans,pc))
    marklist=sorted((value, key) for (key,value) in d.items())
    sortdict=dict([(k,v) for v,k in marklist])
    bestwords = (list(sortdict.keys()))
    bestwords.reverse()
    return bestwords
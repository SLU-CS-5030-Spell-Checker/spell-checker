import random, re, codecs, sys, pickle

#this reads in a txt file and save a list of tuples (frequency, word) in a pickle file
def singleWordFrequency(txt, filename):
    string = open(txt).read().lower()
    freqdict = dict()
    pattern = re.compile(r"([A-Za-z]+)") #removes unneeded punctuation
    for word in re.findall(pattern, string):
        if word in freqdict:	#if word is already accounted for increase count
            freqdict[word] += 1
        else:
            freqdict[word] = 1 #if not create a new word with a count of 1
    words = []
    outfile = open(filename, 'wb')
    for word in sorted(freqdict, key=freqdict.get, reverse=True):
        words.append((freqdict[word],word))
    pickle.dump(words, outfile)  #saved using pickle for ease of indexing
    outfile.close()

#this reads in a txt file and save a dictionary of words and frequency {(word,word): {word:freq}} in a pickle file       
def multiWordFrequency(txt, n, filename):
    answer = ()
    pattern = re.compile(r"([A-Za-z]+)")  #removes unneeded punctuation
    with codecs.open(txt, 'r', 'utf-8') as file:
        for line in file:
            line = line.lower()
            answer = answer + tuple(re.findall(pattern, line))
    model = dict()
    for i in range(len(answer)-n+1):
        key = answer[i:i+n-1]
        val = answer[i+n-1]
        if key in model:
            if val in model[key]:
                model[key][val] += 1 #if key is already accounted for increase count
            else:
                model[key][val] = 1  #if not create a new key
        else:
            model[key] = dict()
            model[key][val] = 1
    outfile = open(filename,'wb')
    pickle.dump(model,outfile)  #saved using pickle for ease of indexing
    outfile.close()



#driver code to create files
textfile = 'shakespeare.txt'

singleWordFrequency(textfile, 'singlewordfreq')

multiWordFrequency(textfile, 3, 'multiwordfreq_n3')

multiWordFrequency(textfile, 2, 'multiwordfreq_n2')




    
    

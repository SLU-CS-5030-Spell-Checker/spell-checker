#from fast_irish import *
#from irish_working import *
from irish_good import *

answers = []
previous = ['','']
endpunct = ['.','?','!']
count = 0

with open('input-test.txt') as f:
    for line in f:
        line = line[:-1]
        count +=1
        temp = line
        
        if line in endpunct:
            previous = ['','']
            
        inpt1 = previous[0]+' '+previous[1]
        inpt2 = line
        lst = correction(inpt1, inpt2)

        if len(lst)>0 and line.isalpha():
            sol = lst[0]
        else:
            sol = line
        previous[0] = previous[1]
        previous[1] = line

        answers.append((line,sol))
        print(count)
        if count > 40:
            break

import csv
with open('test2.tsv','wt') as out_file:
    tsv_output = csv.writer(out_file, delimiter='\t')
    for i in range(len(answers)):
        tsv_output.writerow([answers[i][0], answers[i][1]])

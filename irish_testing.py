from combinedmodels_irish import *

answers = {}
previous = ['','']
endpunct = ['.','?','!']
count = 0

with open('input-test.txt') as f:
	for line in f:
		line = line.strip()
		count +=1
		temp = line
		if line in endpunct:
			previous = ['','']

		inpt = previous[0]+' '+previous[1]+' '+line
		inpt = inpt.lstrip()
		lst = correction(inpt)
		if len(lst)>0:
			sol = lst[0]
		else:
			sol = line
		previous[0] = previous[1]
		previous[1] = temp
        
		answers.update({line:sol})
		print(count)

        
import csv
with open('test.tsv','wt') as out_file:
        tsv_output = csv.writer(out_file, delimiter='\t')
        for key in answers.keys():
                tsv_output.writerow([key, answers[key]])

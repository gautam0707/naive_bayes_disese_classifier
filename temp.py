# used to clean data from csv file

with open('priors.csv','r') as f:
	with open('priors1.csv','w') as w:
		for i in f:
			print(i)
			if len(i) > 6:
				w.write(''.join((i.strip().split('_')[1:]))+'\n')


import csv
with open('twse_list.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
         if row[1][0] == 'F':
                 pass
         else:
             print row[0] ,row[1] 


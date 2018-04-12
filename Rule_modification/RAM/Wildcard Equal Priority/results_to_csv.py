import csv
#from __future__ import division
import os, sys, commands
import time

with open('results.csv', 'w') as csvfile:
    fieldnames = ['Table_Occupancy', 'Latency', 'table_cccupancy' , 'Mean']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for i in range(1, 1401):
    	os.chdir(str(i) + '/')
        print i
        os.system('pwd')
    	f1 = 'flow_delays' + str(i) + '.txt'
    	f2 = 'statistics' + str(i) + '.txt'
    	for line in open(f1):
			line = line.strip()
			words = line.split()
			writer.writerow({'Table_Occupancy': str(i), 'Latency': str(words[1])})
        txt = open(f2, 'r').readlines()
        line = txt[3].strip()
        words = line.split()
        writer.writerow({'table_cccupancy': str(i), 'Mean': str(words[4])})
        os.chdir('..')
        os.system('pwd')

from __future__ import division
import os, sys, commands
import time
#import numpy

initial_rules = sys.argv[1]
nmo_repetitions = sys.argv[2]

flow_mod = 'Modify' + str(initial_rules) + '.txt'

global flow_mod_timestamp
flow_mod_timestamp = {}

global fst_out_timestamp
fst_out_timestamp = {}

count = 1
for line in open(flow_mod):
        line = line.strip()
	words = line.split()
	print words
	srcip = words[1]
	dstip = words[1]
	sec = float(words[3])
	usec = float(words[5])
	flow_mod_timestamp[(count)] = (sec, usec)
	count = count + 1
print "\n"
count = 1
for i in range(1,int(nmo_repetitions)+1):
	fst_out = 'timestamp1-' + str(i) + '.txt'
	for line in open(fst_out):
        	line = line.strip()
        	words = line.split()
        	print words 
        	dstip = words[1]
        	sec = float(words[3])
        	usec = float(words[5])
        	fst_out_timestamp[(count)] = (sec, usec)
        	count = count + 1


f1 = 'flow_delays' + str(initial_rules) + '.txt'
w1 = open(f1,'w')
count = 0
min_delay = 99999999.0
max_delay = -1.0
total_delay = 0.0

for key in flow_mod_timestamp:

	if key in fst_out_timestamp:
		delay= (fst_out_timestamp[key][0] - flow_mod_timestamp[key][0]) * 1000000 + (fst_out_timestamp[key][1] - flow_mod_timestamp[key][1])
		w1.write('%s %f\n' % (key,delay/1000)) #delay in milliseconds
		if min_delay > delay/1000:
			min_delay = delay/1000
		if max_delay < delay/1000:
			max_delay = delay/1000
		total_delay += delay/1000	
		count += 1
 
w1.close()

print 'Delay values in milliseconds'
print 'total rules modified successfully:' , count
print 'total delay for these rules:', total_delay
print 'avg rule insertion delay:', total_delay/count
print 'max rule insertion delay:', max_delay
print 'min rule insertion delay:', min_delay

f3 = "statistics" + str(initial_rules) + ".txt"
w = open(f3,"w")
w.write('Delay values in milliseconds\n')
w.write('Total rules modified successfully: %f\n' % (count))
w.write('Total delay for these rules: %f\n' % (total_delay))
w.write('Avg rule insertion delay: %f\n' % (total_delay/count))
w.write('Max rule insertion delay: %f\n' % (max_delay))
w.write('Min rule insertion delay: %f\n' % (min_delay))
w.close()


print "Creating directory for the results..."
os.system('mkdir ' + str(initial_rules))
print "Moving files to directory..."
os.system('mv ./*.txt ./' + str(initial_rules) + '/')
print "Results moved to directory named: " + str(initial_rules) + "/"

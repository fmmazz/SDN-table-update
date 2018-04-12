from __future__ import division
import os, sys, commands
import time
#import numpy

rounds = sys.argv[1]

for i in xrange(1, int(rounds)+1):

	print "cd round_" + str(i)

	os.chdir("round_" + str(i))

	for j in xrange(50, 1951, 50):

		print "cd " + str(j)
		os.chdir(str(j))

		print "Unzipping tcpdumppacktes-" + str(j) + ".tar.gz"
		os.system("tar -xvzf tcpdumppackets-" + str(j) + ".tar.gz")

		tcpdump = 'tcpdumppacktes' + str(j) + '.txt'
		new_tcpdump = 'timestamp1-1.txt'

		global fst_out_timestamp
		fst_out_timestamp = {}

		print "Opening tcpdumppackets.txt"
		count = 1
		f = open("tcpdumppackets" + str(j) + ".txt", "r") 
		content = f.readlines() 
		f.seek(0)
		num_lines = sum(1 for line in f)
		if not content[num_lines-1]:
			print content[num_lines-1]
			latency = content[num_lines-1].split()
			time = latency[0].split(".")
			sec = float(time[0])
			usec = float(time[1])
			fst_out_timestamp[(count)] = (sec, usec)
		else:
			print content[num_lines-2]
			latency = content[num_lines-2].split()
			time = latency[0].split(".")
		        sec = float(time[0])
		        usec = float(time[1])
		        fst_out_timestamp[(count)] = (sec, usec)

		w1 = open(new_tcpdump,'w')
		print "Saving timestamp1-1.txt"
		print fst_out_timestamp[1][0],fst_out_timestamp[1][1]
		w1.write('dst: 172.31.10.1 sec %d usec %d\n' % (fst_out_timestamp[1][0],fst_out_timestamp[1][1]))

		print "Zipping tcpdumppacktes-" + str(j) + ".tar.gz"
		os.system("tar -czvf tcpdumppackets-" + str(j) + ".tar.gz tcpdumppackets" + str(j) + ".txt")
	
		os.system("rm tcpdumppackets-" + str(j) + ".tar.gz")
		os.system("rm tcpdumppackets" + str(j) + ".txt")

		os.chdir("..")
	os.chdir("..")

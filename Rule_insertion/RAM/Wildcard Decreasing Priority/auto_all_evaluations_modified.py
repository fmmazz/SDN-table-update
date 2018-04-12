import os
import time
import sys
import subprocess

initial_rules_begin = sys.argv[1]
initial_rules_end = sys.argv[2]
number_repetitions = sys.argv[3]

print "BEGIN"
for i in xrange(1, int(number_repetitions)+1):
	for initial_rules in xrange(int(initial_rules_begin),int(initial_rules_end)+1, 50):
		os.system('sudo python auto_sh.py 1 ' + str(initial_rules) + ' 1')

	os.system('mkdir round_' + str(i))
	os.system('mv ./1*/ ./2*/ ./3*/ ./4*/ ./5*/ ./6*/ ./7*/ ./8*/ ./9*/ -t ./round_' + str(i))
	time.sleep(10)

print "END"
sys.exit()

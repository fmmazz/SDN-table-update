import os
import time
import sys
import subprocess

packets = sys.argv[1]
initial_rules = sys.argv[2]
number_repetitions = sys.argv[3]

ipv4_src = "192.168.10.1"
#cmd = 'sudo python pktgen-v3.py ' + str(packets) + ' ' + str (ipv4_src) + ' 45678 &'

os.system('sudo python file_changer.py add_wildcard_high_priority_intercalationv3_sh.py ' + str(initial_rules))

print "BEGIN ----- Initial Rules: " + str(initial_rules) + " -----"
for i in xrange(1,int(number_repetitions)+1):
	print "------ " + str(i) + " -------"
	#call the RYU script
	os.system('sudo bash call_ryu_sh.sh ' + str(packets) + ' &')
	time.sleep(245)

#call the script that calculates mean and organize results files
os.system('sudo python parse_controlv2.py ' + str(initial_rules) + ' ' + str(number_repetitions))

print "END  ----- Initial Rules: " + str(initial_rules) + " -----"
sys.exit()

import os, sys

for i in xrange(int(sys.argv[1]), int(sys.argv[2])+1):
	os.chdir("round_" + str(i))
	for j in xrange(50, 1951, 50):
		os.chdir(str(j))
		os.system("tar -czvf tcpdumppackets-" + str(j) + ".tar.gz tcpdumppackets" + str(j) + ".txt")
		os.system("rm tcpdumppackets" + str(j) + ".txt")
		os.chdir("..")
	os.chdir("..")

from sys import argv
import re
#import linecache
#import fileinput

script, filename, initial_rules = argv

txt = open(filename, 'r').readlines()
print txt[23]

txt[23] = 'initial_rules = ' + str(initial_rules) + '\n'

out = open(filename, 'w')
out.writelines(txt)
out.close()


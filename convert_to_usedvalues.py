"""
Create gizmo_paramters.txt-usedvalues from gizmo_parameters.txt 
It just gets rid of comments and whitespace and writes to STDOUT.

Usage: python convert_to_usedvalues.py gizmo_parameters.txt
"""
import sys

fn_in = sys.argv[1]
f_in = open(fn_in, 'r')
for line in f_in:
    line = line.strip()
    if line.startswith('%') or line.startswith('#') or line == "":
        continue
    line_list = line.split()
    print("%-34s %s" % (line_list[0], line_list[1]))
f_in.close()

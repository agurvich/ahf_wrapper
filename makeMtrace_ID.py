from os import listdir
from os.path import isfile, join
import sys

# Input arguments
snap_dir = sys.argv[1]

Mtrace_ID_file = "Mtrace_ID.txt"
min_halo_rank = 0
max_halo_rank = 19

f = open(snap_dir + "/" + Mtrace_ID_file, 'w')
for i in range(min_halo_rank, max_halo_rank+1):
  f.write(str(i) + "\n")  
f.close()

print('Done making {}!'.format(Mtrace_ID_file))

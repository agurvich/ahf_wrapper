from os import listdir
from os.path import isfile, join
import sys

# Input arguments
snap_dir = sys.argv[1]

snap_num_start = int(sys.argv[2])
snap_num_end = int(sys.argv[3])
snap_step = int(sys.argv[4])

# Make the snap id list.
snap_id_list = range(snap_num_start, snap_num_end + snap_step, snap_step)

MTSnaps_file = "MTSnaps.txt"

snap_id_str_list = []
for i in range(0, len(snap_id_list)):
  snap_id = snap_id_list[i] 
  snap_id_str = str(snap_id)

  if len(snap_id_str)<3:
    snap_id_str = "0" + snap_id_str
  if len(snap_id_str)<3:
    snap_id_str = "0" + snap_id_str

  snap_id_str_list.append(snap_id_str)

# Extract names of all .AHF_halos files and sort them in order of
# snapshot ID.
onlyfiles = [ f for f in listdir(snap_dir) if isfile(join(snap_dir,f)) ]

halo_files = []
for file in onlyfiles:
  if ".AHF_halos" in file:
    
    # Filter halo files on snap_id.
    snap_id_str_file = file[4:7]

    #print "snap_id_str_file=",
    #print snap_id_str_file

    if snap_id_str_file in snap_id_str_list:
      halo_files.append(file)

halo_files.sort()

# Make it search backward
halo_files.reverse()
del halo_files[0]

f = open(snap_dir + "/" + MTSnaps_file, "w")

for file in halo_files:
  f.write(file[:-6] + "\n")  
f.close()

print 'Done making {}!'.format(MTSnaps_file)

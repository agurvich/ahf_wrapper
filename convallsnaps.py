import os
import sys
import subprocess
from HDF5converter import convert

snap_dir = sys.argv[1]

snap_id_min = 90
#snap_id_min = 190
#snap_id_max = 190
#snap_id_min = 190
snap_id_max = 440
snap_id_step = 1

for snap_id in range(snap_id_min, snap_id_max+1, snap_id_step):
  
  snap_id_str = str(snap_id)

  if len(snap_id_str)<3:
    snap_id_str = "0" + snap_id_str
  if len(snap_id_str)<3:
    snap_id_str = "0" + snap_id_str

  file_case = snap_dir + "/snapshot_" + snap_id_str + ".hdf5"
  dir_case = snap_dir + "/snapdir_" + snap_id_str
  if os.access(file_case, os.F_OK):
    rootdir = file_case
  elif os.access(dir_case, os.F_OK):
    rootdir = dir_case
  else:
    print "snap_id="
    print snap_id,
    print "not found in",
    print snap_dir
    continue

  print "rootdir=",
  print rootdir

  if os.path.exists(rootdir):
 	  if os.path.isfile(rootdir):
		  convert(rootdir)
	  else:
		  for root, subFolders, files in os.walk(rootdir):
		      for file in files:
		          if (file.find(".hdf5")!=-1):
			  	  convert(root+"/"+file)

  else:
	  print "FILE/PATH DOES NOT EXIST"

import os
import sys
import subprocess
from HDF5converter import convert
import pdb

# Input arguments
snap_dir = sys.argv[1]
out_dir = sys.argv[2]

snap_num_start = int(sys.argv[3])
snap_num_end = int(sys.argv[4])
snap_step = int(sys.argv[5])

# Make the snap id list.
snap_id_list = range(snap_num_start, snap_num_end + snap_step, snap_step)

for snap_id in snap_id_list:

  snap_id_str = str(snap_id)

  if len(snap_id_str)<3:
    snap_id_str = "0" + snap_id_str
  if len(snap_id_str)<3:
    snap_id_str = "0" + snap_id_str

  snapshot_file = "/snapshot_" + snap_id_str + ".hdf5"
  file_case = snap_dir + snapshot_file
  snapshot_dir = "/snapdir_" + snap_id_str
  dir_case = snap_dir + snapshot_dir 

  if os.access(file_case, os.F_OK):
    rootdir = file_case
    snapshot = snapshot_file
  elif os.access(dir_case, os.F_OK):
    rootdir = dir_case
    snapshot = snapshot_dir
  else:
    print("snap_id=")
    print(snap_id,)
    print("not found in",)
    print(snap_dir)
    continue

  print("rootdir=",)
  print(rootdir)


  if os.path.exists(rootdir):
        if os.path.isfile(rootdir):
                convert(snapshot, snap_dir, out_dir)
        else:
                for root, subFolders, files in os.walk(rootdir):
                    for file in files:
                        if (file.find(".hdf5")!=-1):

                            # Divide the filename up into the part we want copied and the part we don't want copied.
                            full_filename = root + '/' + file
                            split_filename = full_filename.split('/')
                            snapshot = '{}/{}'.format(split_filename[-2], split_filename[-1])

                            convert(snapshot, snap_dir, out_dir)

  else:
        print("FILE/PATH DOES NOT EXIST")

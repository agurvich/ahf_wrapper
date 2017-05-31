import os
from os import listdir
from os.path import isfile, join

snap_dir_list = [#"/scratch/01708/cfaucher/B1_hr_Dec5_2013_11",
  #"/scratch/01708/cfaucher/m09_hr_Dec16_2013"]#,
  #"/scratch/01708/cfaucher/m10_hr_Dec9_2013"]#,
  "/scratch/01708/cfaucher/m11_hhr_Jan9_2013"]#,
  #"/scratch/01708/cfaucher/m12qq_hr_Dec16_2013"]#,
  #"/scratch/01708/cfaucher/m12v_mr_Dec5_2013_3"]
  #"/scratch/01708/cfaucher/m13_mr_Dec16_2013"]
  #"/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo506_Jan9_2014"]#,
  #"/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo450_Jan9_2014",#]#,
  #"/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo350_Jan9_2014",
  #"/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo600_Jan9_2014",#]#,
  #"/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo830_Jan9_2014_lean"]#,
  #"/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo400_Jan9_2014",
  #"/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo650_Jan9_2014"]#,
  #"/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo550_Jan9_2014"]

#snap_id_str_list = ["290", "340", "440"]
#snap_id_list = range(190, 441)
#snap_id_list = range(90, 191)
snap_id_list = range(90, 441)
snap_id_str_list = []

for i in range(0, len(snap_id_list)):
  snap_id = snap_id_list[i] 
  snap_id_str = str(snap_id)

  if len(snap_id_str)<3:
    snap_id_str = "0" + snap_id_str
  if len(snap_id_str)<3:
    snap_id_str = "0" + snap_id_str

  snap_id_str_list.append(snap_id_str)

for snap_dir in snap_dir_list:
  # Change current working directory.
  os.chdir(snap_dir)

  # Run MergerTree.
  cmd_str = "/home1/01708/cfaucher/repos/cafg_python/zooms-analysis/sasha_halo/ahf-v1.0-069/bin/MergerTree " + str(len(snap_id_str_list))
  
  #print "cmd_str=",
  #print cmd_str

  os.system(cmd_str)

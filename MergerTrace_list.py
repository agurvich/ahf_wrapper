import os
from os import listdir
from os.path import isfile, join

snap_dir_list = [#"/scratch/01708/cfaucher/B1_hr_Dec5_2013_11",
  #"/scratch/01708/cfaucher/m09_hr_Dec16_2013"]#,
  #"/scratch/01708/cfaucher/m10_hr_Dec9_2013"]#,
  #"/scratch/01708/cfaucher/m11_hhr_Jan9_2013"]#,
  #"/scratch/01708/cfaucher/m12qq_hr_Dec16_2013"]#,
  #"/scratch/01708/cfaucher/m12v_mr_Dec5_2013_3"]
  #"/scratch/01708/cfaucher/m13_mr_Dec16_2013"]
  "/scratch/01708/cfaucher/m13m14_lr_Dec9_2013"]
  #"/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo506_Jan9_2014"]#,
  #"/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo450_Jan9_2014",#]#,
  #"/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo350_Jan9_2014",
  #"/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo600_Jan9_2014",#]#,
  #"/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo830_Jan9_2014_lean"]#,
  #"/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo400_Jan9_2014",
  #"/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo650_Jan9_2014"]#,
  #"/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo550_Jan9_2014"]

for snap_dir in snap_dir_list:
  # Change current working directory.
  os.chdir(snap_dir)

  # Run MergerTrace.
  os.system("/home1/01708/cfaucher/repos/cafg_python/zooms-analysis/sasha_halo/ahf-v1.0-069/bin/MergerTrace Mtrace_ID.txt MTSnaps.txt")

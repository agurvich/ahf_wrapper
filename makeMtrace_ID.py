from os import listdir
from os.path import isfile, join

#snap_dir = "/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo350_Jan9_2014"
#snap_dir = "/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo400_Jan9_2014"
#snap_dir = "/scratch/01708/cfaucher/m12v_lr_Jan_2014"
#snap_dir = "/scratch/01708/cfaucher/m12v_mr_Dec5_2013_3"
snap_dir = "/scratch/01708/cfaucher/B1_hr_Dec5_2013_11"
#snap_dir = "/scratch/01708/cfaucher/m12qq_hr_Dec16_2013"
#snap_dir = "/scratch/01708/cfaucher/m13_mr_Dec16_2013"
Mtrace_ID_file = "Mtrace_ID.txt"
min_halo_rank = 0
max_halo_rank = 19

f = open(snap_dir + "/" + Mtrace_ID_file, 'w')
for i in range(min_halo_rank, max_halo_rank+1):
  f.write(str(i) + "\n")  
f.close()

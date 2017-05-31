import os

#snap_dir = "/scratch/01708/cfaucher/m12v_lr_Jan_2014"
#snap_dir = "/scratch/01708/cfaucher/m12v_mr_Dec5_2013_3"
#snap_dir = "/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo350_Jan9_2014"
#snap_dir = "/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo400_Jan9_2014"
#snap_dir = "/scratch/01708/cfaucher/B1_hr_Dec5_2013_11"
#snap_dir = "/scratch/01708/cfaucher/m12qq_hr_Dec16_2013"
#snap_dir = "/scratch/01708/cfaucher/m13_mr_Dec16_2013"
#snap_dir = "/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo550_Jan9_2014"
#snap_dir = "/scratch/01708/cfaucher/m13m14_lr_Dec9_2013"
snap_dir = "/scratch/01708/cfaucher/m12v_mr_Dec5_2013_3_noFB_lr"
min_halo_rank = 0
max_halo_rank = 19

for i in range(min_halo_rank, max_halo_rank+1):
  halo_rank_str = str(i)
  if len(halo_rank_str)<3:
    halo_rank_str = "0" + halo_rank_str
  if len(halo_rank_str)<3:
    halo_rank_str = "0" + halo_rank_str
  
  cmd_str = "python simplify_halo.py " + snap_dir + "/halo_00" + halo_rank_str + ".dat"
  os.system(cmd_str)

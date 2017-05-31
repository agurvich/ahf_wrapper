from os import listdir
from os.path import isfile, join

#snap_dir = "/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo350_Jan9_2014"
#snap_dir = "/scratch/01708/cfaucher/dm_512_MUSIC_ex_halo400_Jan9_2014"
#snap_dir = "/scratch/01708/cfaucher/m12v_lr_Jan_2014"
#snap_dir = "/scratch/01708/cfaucher/m12v_mr_Dec5_2013_3"
#snap_dir = "/scratch/01708/cfaucher/B1_hr_Dec5_2013_11"
#snap_dir = "/scratch/01708/cfaucher/m12qq_hr_Dec16_2013"
snap_dir = "/scratch/01708/cfaucher/m13_mr_Dec16_2013"
MTSnaps_file = "MTSnaps.txt"

# Extract names of all .AHF_halos files and sort them in order of
# snapshot ID.
onlyfiles = [ f for f in listdir(snap_dir) if isfile(join(snap_dir,f)) ]

halo_files = []
for file in onlyfiles:
  if ".AHF_halos" in file:
    halo_files.append(file)

halo_files.sort()

f = open(snap_dir + "/" + MTSnaps_file, 'w')
for file in halo_files:
  f.write(file[:-6] + "\n")  
f.close()

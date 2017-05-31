import os

# Input arguments
snap_dir = sys.argv[1]

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

print 'Halos simplified.'

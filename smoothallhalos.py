import os
from dataio import *

# Input argument
snap_dir = sys.argv[1]

min_halo_rank = 0
max_halo_rank = 19

for i in range(min_halo_rank, max_halo_rank+1):
  halo_rank_str = str(i)
  if len(halo_rank_str)<3:
    halo_rank_str = "0" + halo_rank_str
  if len(halo_rank_str)<3:
    halo_rank_str = "0" + halo_rank_str

  halo_data_path = snap_dir + "/halo_00" + halo_rank_str + ".datsimple.txt"

  (redshift_arr, halo_ID_arr, host_ID_arr, xpeak_arr, ypeak_arr, zpeak_arr, Rvir_arr, Mvir_arr, Mgas_arr, Mstar_arr, xCOM_arr, yCOM_arr, zCOM_arr) = tuples_to_arrays(read_data(halo_data_path))

  # Don't allow halos to shrink.
  Rvir_max = 0.0
  Mvir_max = 0.0
  Mgas_max = 0.0
  Mstar_max = 0.0

  for j in range(0, len(redshift_arr)):
    # Update maximum radius and masses.
    if Rvir_arr[j]>Rvir_max:
      Rvir_max = Rvir_arr[j]
    if Mvir_arr[j]>Mvir_max:
      Mvir_max = Mvir_arr[j]
    if Mgas_arr[j]>Mgas_max:
      Mgas_max = Mgas_arr[j]
    if Mstar_arr[j]>Mstar_max:
      Mstar_max = Mstar_arr[j]

    # If current radius and masses are lower than previous max, set them to the
    # previous max.
    if Rvir_max>Rvir_arr[j]:
      Rvir_arr[j] = Rvir_max
    if Mvir_max>Mvir_arr[j]:
      Mvir_arr[j] = Mvir_max
    if Mgas_max>Mgas_arr[j]:
      Mgas_arr[j] = Mgas_max
    if Mstar_max>Mstar_arr[j]:
      Mstar_arr[j] = Mstar_max

  # Write 'smoothed' halos files.
  write_data(arrays_to_tuples((redshift_arr, halo_ID_arr, host_ID_arr, xpeak_arr, ypeak_arr, zpeak_arr, Rvir_arr, Mvir_arr, Mgas_arr, Mstar_arr, xCOM_arr, yCOM_arr, zCOM_arr)), halo_data_path + "smooth")

print 'Done smoothing halos.'

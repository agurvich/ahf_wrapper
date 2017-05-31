import os
import sys
import subprocess
import time
from HDF5converter import convert

snap_dir = sys.argv[1]

#snap_id_min = 90
#snap_id_max = 140
#snap_id_min = 140
#snap_id_max = 190
#snap_id_min = 191
#snap_id_max = 240
snap_id_min = 241
snap_id_max = 290
#snap_id_min = 291
#snap_id_max = 340
#snap_id_min = 341
#snap_id_max = 390
#snap_id_min = 391
#snap_id_max = 440
#snap_id_max = 440
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

  AMIGA_input_str = "[AHF]\n"
  AMIGA_input_str = AMIGA_input_str + "# (stem of the) filename from which to read the data to be analysed\n"

  if os.access(file_case, os.F_OK):
    AMIGA_input_str = AMIGA_input_str + "ic_filename    =  " + snap_dir + "/snap_convertedshot_" + snap_id_str + "\n"
  elif os.access(dir_case, os.F_OK):
    AMIGA_input_str = AMIGA_input_str + "ic_filename    =  " + snap_dir + "/snap_converteddir_" + snap_id_str + "/snap_convertedshot_" + snap_id_str + ".\n"

  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "# what type of input file (cf. src/libio/io_file.h)\n" 
  
  if os.access(file_case, os.F_OK):
    AMIGA_input_str = AMIGA_input_str + "ic_filetype       = 60\n"
  elif os.access(dir_case, os.F_OK):
    AMIGA_input_str = AMIGA_input_str + "ic_filetype       = 61\n"

  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "# prefix for the output files\n"
  AMIGA_input_str = AMIGA_input_str + "outfile_prefix    =  " + snap_dir + "/snap" + snap_id_str + "Rpep.\n"
  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "# number of grid cells for the domain grid (1D)\n"
  AMIGA_input_str = AMIGA_input_str + "LgridDomain       = 512\n"
  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "# number of grid cells for the domain grid (1D) (limits spatial resolution to BoxSize/LgridMax)\n"
  AMIGA_input_str = AMIGA_input_str + "LgridMax          = 134217728 \n"
  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "# refinement criterion on domain grid (#particles/cell)\n"
  AMIGA_input_str = AMIGA_input_str + "NperDomCell       = 10\n"
  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "# refinement criterion on all higher resolution grids (#particles/cells)\n"
  AMIGA_input_str = AMIGA_input_str + "NperRefCell       = 50\n"
  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "# particles with velocity v > VescTune x Vesc are considered unbound \n"
  AMIGA_input_str = AMIGA_input_str + "VescTune          = 1.5\n"
  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "# minimum number of particles for a halo\n"
  AMIGA_input_str = AMIGA_input_str + "NminPerHalo       = 100\n"
  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "# normalisation for densities (1: RhoBack(z), 0:RhoCrit(z))\n"
  AMIGA_input_str = AMIGA_input_str + "RhoVir            = 0\n"
  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "# virial overdensity criterion (<0: let AHF calculate it); Rvir is defined via M(<Rvir)/Vol = Dvir * RhoVir\n"
  AMIGA_input_str = AMIGA_input_str + "Dvir              = -1\n"
  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "# maximum radius (in Mpc/h) used when gathering initial set of particles for each halo (should be larger than the largest halo expected)\n"
  AMIGA_input_str = AMIGA_input_str + "MaxGatherRad      = 0.5	\n"
  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "# the level on which to perform the domain decomposition (MPI only, 4=16^3, 5=32^3, 6=64^3, 7=128^3, 8=256^3, etc.)\n"
  AMIGA_input_str = AMIGA_input_str + "LevelDomainDecomp = 6\n"
  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "# how many CPU's for reading (MPI only)\n"
  AMIGA_input_str = AMIGA_input_str + "NcpuReading       = 1\n"
  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "# name of file containing the dark energy relevant tables (only relevant for -DDARK_ENERGY)\n"
  AMIGA_input_str = AMIGA_input_str + "de_filename       = my_dark_energy_table.txt\n"
  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "############################### FILE SPECIFIC DEFINITIONS ###############################\n"
  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "# NOTE: all these factors are supposed to transform your internal units to\n"
  AMIGA_input_str = AMIGA_input_str + "#           [x] = Mpc/h\n"
  AMIGA_input_str = AMIGA_input_str + "#           [v] = km/sec\n"
  AMIGA_input_str = AMIGA_input_str + "#           [m] = Msun/h\n"
  AMIGA_input_str = AMIGA_input_str + "#           [e] = (km/sec)^2\n"
  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "[GADGET]\n"
  AMIGA_input_str = AMIGA_input_str + "GADGET_LUNIT      = 1.e-3\n"
  AMIGA_input_str = AMIGA_input_str + "GADGET_MUNIT      = 1e10\n"
  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "[TIPSY]\n"
  AMIGA_input_str = AMIGA_input_str + "TIPSY_BOXSIZE       = 50.0\n"
  AMIGA_input_str = AMIGA_input_str + "TIPSY_MUNIT         = 4.75e16\n"
  AMIGA_input_str = AMIGA_input_str + "TIPSY_VUNIT         = 1810.1\n"
  AMIGA_input_str = AMIGA_input_str + "TIPSY_EUNIT         = 0.0\n"
  AMIGA_input_str = AMIGA_input_str + "TIPSY_OMEGA0        = 0.24\n"
  AMIGA_input_str = AMIGA_input_str + "TIPSY_LAMBDA0       = 0.76\n"
  AMIGA_input_str = AMIGA_input_str + "\n"
  AMIGA_input_str = AMIGA_input_str + "[ART]\n"
  AMIGA_input_str = AMIGA_input_str + "ART_BOXSIZE         = 20\n"
  AMIGA_input_str = AMIGA_input_str + "ART_MUNIT           = 6.5e8"

  AMIGA_input_file = snap_dir + "/AMIGA.input" + snap_id_str

  f = open(AMIGA_input_file, 'w')
  f.write(AMIGA_input_str)
  f.close()

  cmd_str = "/home1/01708/cfaucher/repos/cafg_python/zooms-analysis/sasha_halo/ahf-v1.0-069/bin/AHF-v1.0-069 " + AMIGA_input_file

  out_str = " > " + snap_dir + "/AMIGA_" + snap_id_str + ".out 2>&1 &"

  print "cmd_str=",
  print cmd_str

  os.system(cmd_str + out_str)

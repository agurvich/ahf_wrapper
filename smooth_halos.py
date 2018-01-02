#!/usr/bin/env python
'''Script for smoothing halo data, with arguments provided at command line.

@author: Zach Hafen
@contact: zachary.h.hafen@gmail.com
@status: Development
'''

import sys

import galaxy_diver.analyze_data.ahf_updater as analyze_ahf

########################################################################
# Input Paramaters
########################################################################

# Get the directory the AHF data is in
sdir = sys.argv[1]

# Get the directory where the snapshot times are located
snapshot_times_dir = sys.argv[2]

if len( sys.argv ) <= 3:
  index = None
else:
  index = sys.argv[3]

  # Get the right type
  if index != 'snum':
    index = int( index )

########################################################################
# Perform the calculation.
########################################################################

ahf_updater = analyze_ahf.HaloUpdater( sdir )
ahf_updater.save_smooth_mtree_halos( snapshot_times_dir, index=index, )


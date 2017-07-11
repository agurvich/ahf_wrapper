#!/usr/bin/env python
'''Script for getting additional information from the AHF halos files and saving those as additional files.
This is primarily designed for getting the analytic concentration.

@author: Zach Hafen
@contact: zachary.h.hafen@gmail.com
@status: Development
'''

import sys

import galaxy_diver.read_data.ahf as read_ahf

########################################################################
# Input Paramaters
########################################################################

# Get the directory the AHF data is in
sdir = sys.argv[1]

# Get the directory where the snapshot times are located
metafile_dir = sys.argv[2]

# Get the snapshots to process the AHF halo files for
snum = int( sys.argv[3] )

########################################################################
# Perform the calculation.
########################################################################

ahf_reader = read_ahf.AHFReader( sdir )
ahf_reader.save_ahf_halos_add( snum, metafile_dir )


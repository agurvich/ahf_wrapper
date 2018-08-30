#!/usr/bin/env python
'''Script for making sure all the AHF files we need exist.

@author: Zach Hafen
@contact: zachary.h.hafen@gmail.com
@status: Development
'''

import os
import sys

import galaxy_dive.read_data.ahf as read_ahf

########################################################################
# Input Paramaters
########################################################################

# Get the directory the AHF data is in
sdir = os.path.abspath( sys.argv[1] )

# Get the indices
snum_start = int( sys.argv[2] )
snum_end = int( sys.argv[3] )
snum_step = int( sys.argv[4] )

if len( sys.argv ) > 5:
  file_str = sys.argv[5]
else:
  file_str = 'AHF_halos'

########################################################################
# Perform the calculation.
########################################################################

ahf_reader = read_ahf.AHFReader( sdir )
assert ahf_reader.check_files_exist( snum_start, snum_end, snum_step, file_str )


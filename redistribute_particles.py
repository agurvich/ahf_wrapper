#!/usr/bin/env python
'''Script for loading in a snapshot, then resaving it, broken into more even file sizes.

@author: Zach Hafen
@contact: zachary.h.hafen@gmail.com
@status: Development
'''

import sys

import galaxy_diver.utils.hdf5_wrapper as hdf5_wrapper

########################################################################
# Input Paramaters
########################################################################

# Get the directory the AHF data is in
sdir = '/scratch/projects/xsede/GalaxiesOnFIRE/m12m_res7000/output'
copy_dir = '/scratch/03057/zhafen/m12m_res7000/output'

snums = [ 55, 76, 82, 129, 162, ]

########################################################################
# Copy and redistribute
########################################################################

for snum in snums:
  print( "########################################################################" )
  print( "Copying snum {}...".format( snum ) )
  hdf5_wrapper.copy_snapshot( sdir, snum, copy_dir, redistribute=True )


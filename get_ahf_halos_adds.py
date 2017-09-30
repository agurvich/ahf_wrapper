#!/usr/bin/env python
'''Script for getting additional information from the AHF halos files and saving those as additional files.
This is primarily designed for getting the analytic concentration.

@author: Zach Hafen
@contact: zachary.h.hafen@gmail.com
@status: Development
'''

import sys

import galaxy_diver.analyze_data.ahf as analyze_ahf

########################################################################
# Input Paramaters
########################################################################

# Get the directory the AHF data is in
sdir = sys.argv[1]

kwargs = {

  # Get the snapshots to process the AHF halo files for
  'snum' : int( sys.argv[2] ),

  # Get the directory where the snapshot times are located
  'metafile_dir' : sys.argv[3],

  'radii_mass_fractions' : [ 0.5, 0.75, 0.99 ],

  'simulation_data_dir' : sys.argv[4],

  'galaxy_cut' : float( sys.argv[5] ),

  'length_scale' : sys.argv[6],
}

########################################################################
# Perform the calculation.
########################################################################

ahf_updater = analyze_ahf.AHFUpdater( sdir )
ahf_updater.save_ahf_halos_add( **kwargs )


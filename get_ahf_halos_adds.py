#!/usr/bin/env python
'''Script for getting additional information from the AHF halos files and saving those as additional files.
This is primarily designed for getting the analytic concentration.

@author: Zach Hafen
@contact: zachary.h.hafen@gmail.com
@status: Development
'''

import sys

import galaxy_dive.analyze_data.ahf_updater as analyze_ahf

########################################################################
# Input Paramaters
########################################################################

# Get the directory the AHF data is in
sdir = sys.argv[1]

mass_radii_kwargs = {
    'mass_fractions' : [ 0.5, 0.75, 0.9, 0.95, 0.99 ],
    'galaxy_cut' : float( sys.argv[5] ),
    'length_scale' : sys.argv[6],
}

########################################################################
# Perform the calculation.
########################################################################

ahf_updater = analyze_ahf.HaloUpdater( sdir )
ahf_updater.save_halos_add(
    snum = int( sys.argv[2] ),
    metafile_dir = sys.argv[3],
    simulation_data_dir = sys.argv[4],
    mass_radii_kwargs = mass_radii_kwargs,
    include_enclosed_mass = False,
    include_average_quantity_inside_galaxy = False,
    include_v_circ = False,
)

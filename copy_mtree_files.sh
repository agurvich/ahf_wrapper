#!/bin/bash
########################################################################
# Input Arguments
########################################################################

# What snapshots to use
snap_num_start=570
snap_num_end=599
snap_step=1

########################################################################

# Stop on errors
set -e

for (( i = $snap_num_end; i >= $snap_num_start; i = i - $snap_step ))
do
  
  # Store the previous name
  prev_name=(snap$i*mtree)
  echo Previously at $prev_name

  # Save in a new location
  save_name=old_$prev_name
  echo Saving at $save_name
  cp $prev_name "old_"$prev_name

done
  

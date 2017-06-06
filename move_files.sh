#!/bin/bash
########################################################################
# Input Arguments
########################################################################

# What snapshots to use
snap_num_start=571
snap_num_end=599
snap_step=1

########################################################################

# Stop on errors
set -e

for (( i = $snap_num_end; i >= $snap_num_start; i = i - $snap_step ))
do
  
  # Setup the variables
  prev_name=(snap$i*mtree_idx)
  #new_name="${prev_name/$i/$((i-1))}"
  new_name=(snap$(($i+1))*mtree_idx)
  echo Moving $prev_name to $new_name

  mv $prev_name $new_name

done
  
echo Done moving.

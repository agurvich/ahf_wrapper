#!/bin/bash
########################################################################
# Input Arguments
########################################################################

# What simulation to use, and where to put the output
snap_dir=/scratch/03057/zhafen/m12v_mr_Dec5_2013_3
out_dir=/scratch/03057/zhafen/m12v_mr_Dec5_2013_3

# What snapshots to use
snap_num_start=1
snap_num_end=440
snap_step=1

# How many processors to use? (Remember to account for memory constraints)
n_procs=24

# What steps should be done
convert_snapshots=false
find_halos=false
find_merger_tree=false
find_merger_trace=false
smooth_halos=true

########################################################################
# Advanced options, for the smoothing step only
########################################################################

# Where is the file containing the snapshot times located?
snap_times_dir=/scratch/03057/zhafen/m12v_mr_Dec5_2013_3

# What index to use for halo files?
# Be careful about setting this!
# Should be set to $snap_num_end, but *only* if $snap_step == 1.
# If these conditions aren't met, then smoothing currently isn't available.
index=440

########################################################################
# Pipeline Script
########################################################################

# Stop on errors
set -e

echo 
echo '########################################################################'
echo Starting up
echo '########################################################################'

echo Using data in $snap_dir
echo Saving data in $out_dir
pipeline_location=$( pwd )
echo Starting in $pipeline_location

########################################################################

if $convert_snapshots; then

  echo 
  echo '########################################################################'
  echo Converting snapshots
  echo '########################################################################'

  seq $snap_num_start $snap_step $snap_num_end | xargs -n 1 -P $n_procs sh -c 'python convsnaps_list.py $0 $1 $2 $2 1' $snap_dir $out_dir
  echo Done converting snapshots!
  echo 

else
  echo Skipping snapshot conversion.
fi
########################################################################

if $find_halos; then

  echo 
  echo '########################################################################'
  echo Running AHF
  echo '########################################################################'

  # Make input files for AHF
  python findhalos_list.py $out_dir $snap_num_start $snap_num_end $snap_step

  # Run AHF.
  echo Now running AHF!
  seq -f '%03g' $snap_num_start $snap_step $snap_num_end | xargs -n 1 -P $n_procs sh -c './ahf-v1.0-069/bin/AHF-v1.0-069 $0/AMIGA.input$1 > $0/AMIGA_$1.out 2>&1' $out_dir
  # The above command is really complicated, so let me explain below, to the best of my abilities.
  # Everything to the left of the pipe is setting up a sequence of numbers, with some special formatting.
  # To the right we have xargs, which receives the things to the left and starts up multiprocessing.
  # After the sh in to the right is setting up its own mini command window. It receives the piped number as the second argument, the $1. The first argument then is the $out_dir.

else
  echo Skipping finding halos.
fi

########################################################################

if $find_merger_tree; then

  echo 
  echo '########################################################################'
  echo Running MergerTree
  echo '########################################################################'

  # Prepare MergerTree for running
  cd $pipeline_location
  echo Running makeMTSnaps_list.py
  python makeMTSnaps_list.py $out_dir $snap_num_start $snap_num_end $snap_step
  echo Running makeMtrace_ID.py
  python makeMtrace_ID.py $out_dir

  echo Switching to the output directory, $out_dir
  cd $out_dir

  # Run MergerTree
  num_snaps=$( cat $out_dir/MTSnaps.txt | wc -l )
  echo Tracking for $num_snaps snapshots.
  $pipeline_location/ahf-v1.0-069/bin/MergerTree $num_snaps

else
  echo Skipping MergerTree.
fi

########################################################################

if $find_merger_trace; then

  echo 
  echo '########################################################################'
  echo Running MergerTrace
  echo '########################################################################'

  if ! $find_merger_tree; then
    # Prepare MergerTrace for running
    cd $pipeline_location
    echo Running makeMTSnaps_list.py
    python makeMTSnaps_list.py $out_dir $snap_num_start $snap_num_end $snap_step
    echo Running makeMtrace_ID.py
    python makeMtrace_ID.py $out_dir
  fi

  echo Switching to the output directory, $out_dir
  cd $out_dir

  # Run MergerTrace
  $pipeline_location/ahf-v1.0-069/bin/MergerTrace Mtrace_ID.txt MTSnaps.txt

  echo Done with MergerTrace.

else
  echo Skipping MergerTrace.
fi

########################################################################

if $smooth_halos; then

  echo 
  echo '########################################################################'
  echo Simplifying and Smoothing Halos
  echo '########################################################################'

  echo Moving to the pipeline location
  cd $pipeline_location

  echo Smoothing halos
  python smooth_halos.py $out_dir $snap_times_dir $index

else
  echo Skipping smoothing.
fi

########################################################################

echo 
echo All done!!!
echo 

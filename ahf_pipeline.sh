#!/bin/bash

# Input Arguments

# What simulation to use, and where to put the output
snap_dir=/scratch/projects/xsede/GalaxiesOnFIRE/metaldiff/m12i_res7000_md/output
out_dir=/scratch/03057/zhafen/m12i_res7000_md/output

# What snapshots to use
snap_num_start=380
snap_num_end=600
snap_step=10

# What steps should be done
convert_snapshots=false
find_halos=true
find_merger_history=false
simplify_and_smooth_halos=false

# How many processors to use? (Remember to account for memory constraints)
n_procs=16

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

  python convsnaps_list.py $snap_dir $out_dir $snap_num_start $snap_num_end $snap_step
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

  ## Iterate over snapshots
  #for i in $( eval echo "{$snap_num_start..$snap_num_end..$snap_step}" )
  #do
  #  printf -v padded_i "%03d" $i # Get a padded i, for consistent file names
  #  echo Starting AHF for snap $padded_i
  #  echo ./ahf-v1.0-069/bin/AHF-v1.0-069 $out_dir/AMIGA.input$i
  #  ./ahf-v1.0-069/bin/AHF-v1.0-069 $out_dir/AMIGA.input$i > $out_dir/AMIGA_${padded_i}.out 2>&1 &
  #done
  #echo Running... Wait for completion... &
  #wait
  #echo Finished finding halos!

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

if $find_merger_history; then

  echo 
  echo '########################################################################'
  echo Running MergerTree and MergerTrace
  echo '########################################################################'

  # Prepare the files for running
  python makeMTSnaps_list.py $out_dir $snap_num_start $snap_num_end $snap_step
  python makeMtrace_ID_list.py $out_dir

  echo Switching to the output directory, $out_dir
  cd $out_dir

  # Run MergerTree
  num_snaps=$( cat $out_dir/MTSnaps.txt | wc -l )
  echo Tracking for $num_snaps snapshots.
  $pipeline_location/ahf-v1.0-069/bin/MergerTree $num_snaps
  # Check if it failed
  if [ $? -eq 0 ]; then
      echo OK
  else
      echo FAIL
  fi

  # Run MergerTrace
  $pipeline_location/ahf-v1.0-069/bin/MergerTrace Mtrace_ID.txt MTSnaps.txt

  echo Done with MergerTree and MergerTrace.
  echo Leaving output directory.
  echo Returning to pipeline directory, $pipeline_location

else
  echo Skipping MergerTree and MergerTrace.
fi

########################################################################

if $simplify_and_smooth_halos; then

  echo 
  echo '########################################################################'
  echo Simplifying and Smoothing Halos
  echo '########################################################################'

  # Simplify halos
  python simphalos_list.py $out_dir
  python smoothallhalos.py $out_dir

else
  echo Skipping smoothing and simplifying.
fi

########################################################################

echo 
echo All done!!!
echo 

#!/bin/bash

#SBATCH --job-name=ahf_pipeline
#SBATCH --partition=largemem
## Stampede node has 16 processors & 32 GB
## Except largemem nodes, which have 32 processors & 1 TB
#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --time=36:00:00
#SBATCH --output=/scratch/03057/zhafen/m12v_mr_Dec5_2013_3/halo_0.2Rvir/jobs/%j.out
#SBATCH --error=/scratch/03057/zhafen/m12v_mr_Dec5_2013_3/halo_0.2Rvir/jobs/%j.err
#SBATCH --mail-user=zhafen@u.northwestern.edu
#SBATCH --mail-type=begin
#SBATCH --mail-type=fail
#SBATCH --mail-type=end
#SBATCH --account=TG-AST140023

########################################################################
# Input Arguments
########################################################################

# What simulation to use, and where to put the output
snap_dir=/scratch/03057/zhafen/m12v_mr_Dec5_2013_3
out_dir=/scratch/03057/zhafen/m12v_mr_Dec5_2013_3/halo_0.2Rvir

# What snapshots to use
snap_num_start=1
snap_num_end=440
snap_step=1

# How many processors to use? (Remember to account for memory constraints)
n_procs=30

# What steps should be done
convert_snapshots=false
find_halos=false
find_merger_tree=false
find_merger_trace=false
get_ahf_halos_adds=true
smooth_halos=true

########################################################################
# Advanced options, for adding to the AHF data
########################################################################

# Where are the metafiles (e.g. the file containing the snapshot times located)?
metafile_dir=/scratch/03057/zhafen/m12v_mr_Dec5_2013_3

# When getting the effective radii, we use the stellar mass inside galaxy_cut*length_scale of the halo.
galaxy_cut=0.2
length_scale=R_vir

# What index to use for halo files?
# Be careful about setting this!
# Should be set to $snap_num_end, but *only* if $snap_step == 1.
# If these conditions aren't met, then smoothing currently isn't available.
index=$snap_num_end

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

  echo Checking that all AHF snapshots were created successfully...
  $pipeline_location/check_ahf_files_exist.py $out_dir $snap_num_start $snap_step $snap_num_end
  echo Success!

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

if $get_ahf_halos_adds; then

  echo 
  echo '########################################################################'
  echo Generating *.AHF_halos_add files
  echo '########################################################################'

  echo Moving to the pipeline location
  cd $pipeline_location

  echo Getting additional AHF_halos information.
  seq $snap_num_start $snap_step $snap_num_end | xargs -n 1 -P $n_procs sh -c 'python get_ahf_halos_adds.py $0 $5 $1 $2 $3 $4' $out_dir $metafile_dir $snap_dir $galaxy_cut $length_scale

else
  echo Skipping getting additional AHF_halos information.
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
  python smooth_halos.py $out_dir $metafile_dir $index

else
  echo Skipping smoothing.
fi

########################################################################

echo 
echo All done!!!
echo 

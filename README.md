# README #

This repository is designed for easily running [Amiga Halo Finder](http://popia.ft.uam.es/AHF/Documentation.html) on the FIRE simulations.
It uses a significant amount of code written by Sasha Muratov.

### Set Up ###

1. Clone the repository with `git clone git@bitbucket.org:zhafen/ahf_wrapper.git`.
2. Move into the AHF subdir (e.g. `ahf-v1.0-069`), and make AHF (i.e. `make clean; make`).
3. Clone my general analysis repository Galaxy Diver (located at git@bitbucket.org:zhafen/galaxy_diver.git), and add it to your path.
4. If you want the halo concentration, then you'll need to install [Colossus](http://www.benediktdiemer.com/code/colossus/)

In the future, I hope to make this installation process more automatic.

### Usage ###

To run AHF, simply consider making the following edits to `ahf_pipeline.sh`, and then submit it as a job.

1. Go through each of the slurm job submission options, and make sure that they are relevant. E.g. does the output go where you want? Do you have the queue specified? Are you mailing the right user?
2. Change snap_dir to the location of the simulation data.
3. Change out_dir to the location you want the halo data output too. *Do not send the output to the shared FIRE folder*. AHF produces several hundred GB of halo data, in addition to a *full copy* of the simulation output converted to binary, which can and should be deleted later on.
4. Specify where the simulation metafiles are located (e.g. the file containing the snapshot times).
5. Choose the snapshot range you want this use.
6. Choose how many processors you want to use.
7. Choose if you want to convert snapshots to binary (`convert_snapshots`; AHF reads in binary files, so this step is typically essential).
8. Choose if you want to run AHF itself (`find_halos`; also essential).
9. Choose if you want to correlate halos between files (`find_merger_tree`; usually important).
10. Choose if you want to trace particular halos through the entire simulation (`find_merger_trace`; usually important)
11. Choose if you want to get extra information about each halo not usually included by AHF (`get_ahf_halos_adds`; this is optional, and includes information like the stellar half-mass radius, the halo concentration, mass contained within the stellar half-mass radius, and more).
12. Choose if you want to smooth halos (`smooth_halos`; optional, but useful).

### Troubleshooting ###
If the pipeline fails, the most common issue is a corrupted snapshot, so check the raw data. Many snapshots directories often contain hidden files (e.g. `.snapshot_014.1.hdf5.aKDJLd`), which can often also cause problems. The pipeline can also run out of memory if you have too many processes running at once.

### Who do I talk to? ###

Contact Zach Hafen (zachary.h.hafen@gmail.com) with any questions or problems.
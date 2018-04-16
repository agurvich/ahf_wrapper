import readsnapHDF5 as rs
import numpy as np
import sys
import os
import errno

import pdb

#select I/O fields to convert
#will be ordered in the same way listed here
#blocks_to_write=["POS ", "VEL ", "ID  ", "MASS", "U   ", "RHO ", "VOL ", "CMCE", "AREA", "NFAC", "NE  ", "NH  ", "HSML", "SFR ", "AGE ", "Z   "]

blocks_to_write=["POS ", "VEL ", "ID  ", "MASS", "U   ", "RHO ", "NE  ", "NH  ", "HSML", "SFR ", "AGE ", "Z   "]

########################################################################

def mkdirP(path):
  '''Make a path to a file.'''

  try:
    os.makedirs(path)
  except OSError as exc: # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else: raise

  return 0

########################################################################

def convert(filename_in, snap_dir, out_dir):
    filename_in = filename_in.replace(".hdf5","")

    if (filename_in.find("arepo")>=0):
        filename_out = filename_in.replace("arepo", "arepo_converted")
    else:
        if(filename_in.find("snap")>=0):
            filename_out=filename_in.replace("snap", "snap_converted")
        else:
            filename_out = filename_in + "_converted"

        
    # Get the full filenames
    full_filename_in = snap_dir + '/' + filename_in
    full_filename_out = out_dir + '/' + filename_out

    # Make the output directory
    snapshot_dir = filename_out.split('/')[0]
    full_output_dir = '{}/{}'.format(out_dir, snapshot_dir)
    mkdirP(full_output_dir)

    # Create the new file
    f = open(full_filename_out ,'wb')

    print(full_filename_in + " --> " + full_filename_out)

    print("  HEADER")
    header = rs.snapshot_header(full_filename_in)
    print("  npart    = ", header.npart)
    print("  redshift = ", header.redshift)
    print("  massarr  = ", header.massarr)
    print("  double   = ", header.double)
    blocksize=np.array([256],dtype=np.uint32)
    blocksize.tofile(f)
    header.npart.tofile(f)
    header.massarr.tofile(f)
    header.time.tofile(f)
    header.redshift.tofile(f)
    header.sfr.tofile(f)
    header.feedback.tofile(f)
    header.nall.tofile(f)
    header.cooling.tofile(f)
    header.filenum.tofile(f)
    header.boxsize.tofile(f)
    header.omega0.tofile(f)
    header.omegaL.tofile(f)
    header.hubble.tofile(f)
    header.stellar_age.tofile(f)
    header.metals.tofile(f)
    header.nall_highword.tofile(f)
    sizeof=header.npart.dtype.itemsize*header.npart.size + header.massarr.dtype.itemsize*header.massarr.size + header.time.dtype.itemsize*header.time.size + header.redshift.dtype.itemsize*header.redshift.size + header.sfr.dtype.itemsize*header.sfr.size + header.feedback.dtype.itemsize*header.feedback.size +header.nall.dtype.itemsize*header.nall.size +header.cooling.dtype.itemsize*header.cooling.size +header.filenum.dtype.itemsize*header.filenum.size +header.boxsize.dtype.itemsize*header.boxsize.size +header.omega0.dtype.itemsize*header.omega0.size +header.omegaL.dtype.itemsize*header.omegaL.size +header.hubble.dtype.itemsize*header.hubble.size +header.stellar_age.dtype.itemsize*header.stellar_age.size +header.metals.dtype.itemsize*header.metals.size +header.nall_highword.dtype.itemsize*header.nall_highword.size

    filldata=np.zeros(256-sizeof,dtype=np.byte)
    filldata.tofile(f)
    blocksize.tofile(f)
    print("  ..written bytes...", f.tell())

    for i in range(0,len(blocks_to_write)):
        if rs.contains_block(full_filename_in+".hdf5", blocks_to_write[i]):
            data = rs.read_block(full_filename_in, blocks_to_write[i], no_mass_replicate=True)
            print(" ", blocks_to_write[i], data.dtype.itemsize, data.size)
            sizeof=data.dtype.itemsize*data.size
            blocksize=np.array([sizeof],dtype=np.uint32)
            blocksize.tofile(f)
            data.tofile(f)
            blocksize.tofile(f)
            print("  ...written bytes...", f.tell())

    f.close()

if __name__=="__main__":
    rootdir = sys.argv[1]

    if os.path.exists(rootdir):
        if os.path.isfile(rootdir):
            convert(rootdir)
        else:
            for root, subFolders, files in os.walk(rootdir):
                for file in files:
                    if (file.find(".hdf5")!=-1):
                        convert(root+"/"+file)

    else:
        print("FILE/PATH DOES NOT EXIST")

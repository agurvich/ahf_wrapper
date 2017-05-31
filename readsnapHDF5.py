# import readsnapHDF5 as rs
# header = rs.snapshot_header("snap_063.0") 
# mass = rs.read_block("snap_063","MASS",parttype=5) # reads mass for particles of type 5, using block names should work for both format 1 and 2 snapshots
#
# before using read_block, make sure that the description (and order if using format 1 snapshot files) of the data blocks
# is correct for your configuration of Gadget 
#
# for mutliple file snapshots give e.g. the filename "snap_063" rather than "snap_063.0" to read_block
# for snapshot_header the file number should be included, e.g."snap_063.0", as the headers of the files differ
#
# the returned data block is ordered by particle species even when read from a multiple file snapshot

import numpy as np
import os
import sys
import math
import tables

############ 
#DATABLOCKS#
############
#descriptions of all datablocks -> add datablocks here!
#TAG:[HDF5_NAME,DIM]
datablocks = {"POS ":["Coordinates",3], 
	      "VEL ":["Velocities",3],
	      "ID  ":["ParticleIDs",1],
	      "MASS":["Masses",1],
              "U   ":["InternalEnergy",1],
              "RHO ":["Density",1],
              "VOL ":["Volume",1],
              "CMCE":["Center-of-Mass",3],
              "AREA":["Surface Area",1],
              "NFAC":["Number of faces of cell",1],
              "NE  ":["ElectronAbundance",1],
              "NH  ":["NeutralHydrogenAbundance",1],
	      "HSML":["SmoothingLength",1],
              "SFR ":["StarFormationRate",1],
              "AGE ":["StellarFormationTime",1],
              "Z   ":["Metallicity",1],
	      "ACCE":["Acceleration",3],
              "VEVE":["VertexVelocity",3],
              "FACA":["MaxFaceAngle",1],              
	      "COOR":["CoolingRate",1],
              "POT ":["Potential",1],
	      "MACH":["MachNumber",1]}	

########################### 
#CLASS FOR SNAPSHOT HEADER#
###########################  
class snapshot_header:
  def __init__(self, filename):
 
    if os.path.exists(filename):
        curfilename=filename
    elif os.path.exists(filename+".hdf5"):
    	curfilename = filename+".hdf5"
    elif os.path.exists(filename+".0.hdf5"): 
	curfilename = filename+".0.hdf5"
    else:	
	print "[error] file not found : ", filename
    	sys.exit()
    
    f=tables.open_file(curfilename)
 
    self.filename = filename  
    self.npart = f.root.Header._v_attrs.NumPart_ThisFile 
    self.nall = f.root.Header._v_attrs.NumPart_Total
    self.nall_highword = f.root.Header._v_attrs.NumPart_Total_HighWord
    self.massarr = f.root.Header._v_attrs.MassTable 
    self.time = f.root.Header._v_attrs.Time 
    self.redshift = f.root.Header._v_attrs.Redshift 
    self.boxsize = f.root.Header._v_attrs.BoxSize
    self.filenum = f.root.Header._v_attrs.NumFilesPerSnapshot
    self.omega0 = f.root.Header._v_attrs.Omega0
    self.omegaL = f.root.Header._v_attrs.OmegaLambda
    self.hubble = f.root.Header._v_attrs.HubbleParam
    self.sfr = f.root.Header._v_attrs.Flag_Sfr 
    self.cooling = f.root.Header._v_attrs.Flag_Cooling
    self.stellar_age = f.root.Header._v_attrs.Flag_StellarAge
    self.metals = f.root.Header._v_attrs.Flag_Metals
    self.feedback = f.root.Header._v_attrs.Flag_Feedback
    self.double = f.root.Header._v_attrs.Flag_DoublePrecision
     
    f.close()

##############################
#READ ROUTINE FOR SINGLE FILE#
############################## 
def read_block_single_file(filename, block_name, dim2, parttype=-1, no_mass_replicate=False, verbose=False):

  if (verbose):
	  print "[single] reading file           : ", filename   	
	  print "[single] reading                : ", block_name
      
  head = snapshot_header(filename)
  npart = head.npart
  massarr = head.massarr
  nall = head.nall
  filenum = head.filenum
  doubleflag = head.double
  del head

  f=tables.open_file(filename)


  #read specific particle type 
  if parttype>=0:
        if (verbose):
        	print "[single] parttype               : ", parttype 
	if ((block_name=="Masses") & (npart[parttype]>0) & (massarr[parttype]>0)):
	        if (verbose):
			print "[single] replicate mass block"	
		ret_val=np.repeat(massarr[parttype], npart[parttype])
        else:		
	  	part_name='PartType'+str(parttype)
	  	ret_val = f.root._f_get_child(part_name)._f_get_child(block_name)[:]
        if (verbose):
        	print "[single] read particles (total) : ", ret_val.shape[0]/dim2

  #read all particle types
  if parttype==-1:
	first=True
	dim1=0
	for parttype in range(0,6):
		part_name='PartType'+str(parttype)
		if (f.root.__contains__(part_name)):
			if (verbose):
				print "[single] parttype               : ", parttype 
				print "[single] massarr                : ", massarr
				print "[single] npart                  : ", npart

	        	if ((block_name=="Masses") & (npart[parttype]>0) & (massarr[parttype]>0) & (no_mass_replicate==False)):
                       		if (verbose):
                               		print "[single] replicate mass block"
				if (first):
			        	data=np.repeat(massarr[parttype], npart[parttype])
					dim1+=data.shape[0]
					ret_val=data
					first=False
				else:	
					data=np.repeat(massarr[parttype], npart[parttype])	
                                        dim1+=data.shape[0]
                                        ret_val=np.append(ret_val, data)
        	                if (verbose):
                	        	print "[single] read particles (total) : ", ret_val.shape[0]/dim2
                                if (doubleflag==0):
					ret_val=ret_val.astype("float32")
			if (f.root._f_get_child(part_name).__contains__(block_name)):
				if (first):
					data=f.root._f_get_child(part_name)._f_get_child(block_name)[:]
					dim1+=data.shape[0]
					ret_val=data
					first=False
				else:
					data=f.root._f_get_child(part_name)._f_get_child(block_name)[:]
					dim1+=data.shape[0]
					ret_val=np.append(ret_val, data)
                		if (verbose):
                        		print "[single] read particles (total) : ", ret_val.shape[0]/dim2

	if ((dim1>0) & (dim2>1)):
		ret_val=ret_val.reshape(dim1,dim2)

  f.close()

  return ret_val

##############
#READ ROUTINE#
##############
#note: arepo, no_masses arguments just dummies to be compatible with read_block of readsnap for Gadget formats
def read_block(filename, block, parttype=-1, no_mass_replicate=False, verbose=False):
  if (verbose):
          print "reading block          : ", block

  if parttype not in [-1,0,1,2,3,4,5]:
    print "[error] wrong parttype given"
    sys.exit()

  curfilename=filename+".hdf5"

  if os.path.exists(curfilename):
    multiple_files=False
  elif os.path.exists(filename+".0"+".hdf5"):
    curfilename = filename+".0"+".hdf5"
    multiple_files=True
  else:
    print "[error] file not found : ", filename
    sys.exit()

  head = snapshot_header(curfilename)
  filenum = head.filenum
  del head

  if (datablocks.has_key(block)):
        block_name=datablocks[block][0]
        dim2=datablocks[block][1]
        first=True
        if (verbose):
                print "Reading HDF5           : ", block_name
                print "Data dimension         : ", dim2
		print "Multiple file          : ", multiple_files
  else:
        print "[error] Block type ", block, "not known!"
        sys.exit()


  if (multiple_files):	
	first=True
	dim1=0
	for num in range(0,filenum):
		curfilename=filename+"."+str(num)+".hdf5"
		if (verbose):
			print "Reading file           : ", num, curfilename 
		if (first):
			data = read_block_single_file(curfilename, block_name, dim2, parttype, verbose)
			dim1+=data.shape[0]
			ret_val = data
			first = False 
		else:	 
                        data = read_block_single_file(curfilename, block_name, dim2, parttype, verbose)
                        dim1+=data.shape[0]
			ret_val=np.append(ret_val, data)
                if (verbose):
                        print "Read particles (total) : ", ret_val.shape[0]/dim2

	if ((dim1>0) & (dim2>1)):
		ret_val=ret_val.reshape(dim1,dim2)	
  else:
	ret_val=read_block_single_file(curfilename, block_name, dim2, parttype, no_mass_replicate, verbose)

  return ret_val


#############
#LIST BLOCKS#
#############
def list_blocks(filename, parttype=-1, verbose=False):
  
  f=tables.open_file(filename)
  for parttype in range(0,6):
  	part_name='PartType'+str(parttype)
        if (f.root.__contains__(part_name)):
        	print "Parttype contains : ", parttype
		print "-------------------"
		iter = it=datablocks.__iter__()
		next = iter.next()
		while (1):
			if (verbose):
				print "check ", next, datablocks[next][0]
			if (f.root._f_get_child(part_name).__contains__(datablocks[next][0])):
  				print next, datablocks[next][0]
			try:
				next=iter.next()
			except StopIteration:
				break	
  f.close() 

#################
#CONTAINS BLOCKS#
#################
def contains_block(filename, tag, parttype=-1, verbose=False):
  
  contains_flag=False
  f=tables.open_file(filename)
  for parttype in range(0,6):
        part_name='PartType'+str(parttype)
        if (f.root.__contains__(part_name)):
                iter = it=datablocks.__iter__()
                next = iter.next()
                while (1):
                        if (verbose):
                                print "check ", next, datablocks[next][0]
                        if (f.root._f_get_child(part_name).__contains__(datablocks[next][0])):
                                if (next.find(tag)>-1):
					contains_flag=True	
                        try:
                                next=iter.next()
                        except StopIteration:
                                break
  f.close() 
  return contains_flag

############
#CHECK FILE#
############
def check_file(filename):
  f=tables.open_file(filename)
  f.close()
                                                                                                                                                  



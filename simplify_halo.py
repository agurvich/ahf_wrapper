import numpy as np
import sys
import os

if (len(sys.argv) < 2):
	print 'syntax: blah.py filename '
	sys.exit()

	
finname = str(sys.argv[1])

foutname = finname+'simple.txt'
hfile = open(finname)
h_dars = np.loadtxt(hfile)
try:
  halozs = h_dars[:,0]
  haloID = h_dars[:,1]
  host = h_dars[:,2]
  Xc = h_dars[:,6]
  Yc = h_dars[:,7]
  Zc = h_dars[:,8]
  Rvir = h_dars[:,12]
  Mass = h_dars[:,4]
  Mgas = h_dars[:,54]
  Mstar = h_dars[:,74]
  comX = h_dars[:,50]
  comY = h_dars[:,51]
  comZ = h_dars[:,52] 
except IndexError:
  halozs = h_dars[0]
  haloID = h_dars[1]
  host = h_dars[2]
  Xc = h_dars[6]
  Yc = h_dars[7]
  Zc = h_dars[8]
  Rvir = h_dars[12]
  Mass = h_dars[4]
  Mgas = h_dars[54]
  Mstar = h_dars[74]
  comX = h_dars[50]
  comY = h_dars[51]
  comZ = h_dars[52] 

newh = np.column_stack((halozs, haloID, host, Xc, Yc, Zc, Rvir, Mass, Mgas, Mstar, comX, comY, comZ))

print newh
np.savetxt(foutname, newh, fmt='%1.6e')



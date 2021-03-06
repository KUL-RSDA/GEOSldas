#!/usr/bin/env python
#
# module load python/GEOSpyD/Ana2019.03_py3.7
# module load nco/4.8.1
#
# Script for creating ensemble-average land forcing (lfo) files.
#
# Usage:  average_ensemble_forcing.py  [in_path]  [out_path]  [nens]
#
# where 
# 
#   in_path  : path to ensemble of lfo files
#   out_path : path to output ensemble-average lfo files
#   nens     : number of lfo ensemble members
#
# The ensemble of input lfo files must be staged as follows:
#
#   [in_path]/mem[NNN]/[EXPID].[HISTSPECa]_lfo_[HISTSPECb].[YYYYMMDD_HHMM]z.nc4
#
# where
#
#   [in_path]       = command-line argument that specifies the path to the ensemble of lfo files 
#   [NNN]           = three-digit ensemble ID (number from 1 to nens) 
#   [EXPID]         = experiment ID
#   [HISTSPECa/b]   = other specs from HISTORY.rc (e.g., "tavg1_2d", "inst1_2d", "Nx+-")
#   [YYYYMMDD_HHMM] = time stamp
#
# This convention matches the directory/file structure generated by the ensemble component
#   of the GEOS atmospheric data assimilation system (ADAS). 
# The ensemble-average files are created *separately* for each time, for each experiment ID, 
#   and for each distinct HISTORY spec.
# The ensemble-average files are placed in "out_path" (command-line argument)
#   and will have the same name as the corresponding input files.

import sys
import os
import glob
import subprocess as sp

def averaging_forcing(in_path, out_path, nens):
   """ The ensemble number will be appended to in_path starting from 001.
       The out_path will be created if it does not exist. """ 
   if not os.path.exists(out_path):
      os.makedirs(out_path) 
   files_list=[]
   for i in range(1,nens+1):
      sfx = '%03d'%(i)
      folder  = in_path+'/atmens/ensdiag/mem'+sfx
      fs      = sorted(glob.glob(folder+'/*lfo*.nc4'))
      files_list.append(fs)
   for fs in zip(*files_list):
      k = 1
      # verify filenames are the same.
      for f in fs:
         n = f.rindex('/')
         if (k==1):
            f0 = f[n+1:]
            k  = k+1
         f1 = f[n+1:]
         assert f0 == f1, "averaging different files. Each folder should have same files"
      fnames = " ".join(fs)
      cmd = 'ncea ' + fnames + ' ' + out_path +'/' + f0         
      sp.call(cmd, shell=True)
   
if __name__ == '__main__' :
 
   in_path  =     sys.argv[1]
   out_path =     sys.argv[2]
   nens     = int(sys.argv[3])

   averaging_forcing(in_path, out_path, nens)

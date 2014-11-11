#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)

import os
import numpy as np
import glob
import sys
import subprocess

TOL_CORR=0.99
TOL_ERR=1E-04

def run(cmd):
  from env_config import env_dic

  p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       env=env_dic)
  ans, errs = p.communicate()
  rc = p.wait()
  return rc, ans, errs

def CompareAllSeismograms(ref_dir, example_dir):
  """ Compare all the seismograms in example_dir with the ones in ref_dir.

  Args:
    ref_dir: Directory where the reference seismograms are.
    example_dir: Directory for the example.

  Returns:
     True if both tests are satisfied, False otherwise.

  assumption: both directories need to contain a subdirectory OUTPUT_FILES
  """

  print('ref_dir= %s\nexample_dir= %s' % (ref_dir, example_dir))

  files = glob.glob(ref_dir + '/' + '*.sem*')

  files.sort()

  corr_min=1;
  err_max=0.;

  sys.stdout.write("|%-20s| %-13s| %-13s|\n" % ('file name', 'corr', 'err'))

  for f in files:
    # build reference and synthetics file names
    #==========================================
    fname=os.path.basename(f)
    ref=np.loadtxt(ref_dir + fname)[:,1]
    syn=np.loadtxt(example_dir + fname)[:,1]

    # correlation test
    #=================
    corr_mat=np.corrcoef(ref, syn)
    corr=np.min(corr_mat)
    corr_min=min(corr,corr_min)

    # least square test
    #==================
    norm=np.linalg.norm
    sqrt=np.sqrt
    err=norm(ref-syn)/sqrt(norm(ref)*norm(syn))
    err_max=max(err, err_max)

    # print results to screen
    sys.stdout.write("|%20s| %13.5le| %13.5le|\n" % (fname, corr, err))

  # print min(coor) max(err)
  sys.stdout.write("|--------------------------------------------------|\n")
  sys.stdout.write("|%-20s| %13.5le| %13.5le|\n" % ('min/max',
                                                    corr_min, err_max))

  return (corr_min >= TOL_CORR) & (err_max <= TOL_ERR)

if __name__ == '__main__':
  """Runs an example and compare its seismograms with a reference.

  usage: CheckExamples.py code_name example_name ref_top_dir

  It needs to be called from the top directory of the repository e.g. specfem2d.
  This directory needs to contain the EXAMPLES directory.
  The environment variables needed to compile the code are given in a module
  called env_config.py.

  Two measures are used to compare the seismograms:
    - least square defined as
      \[
      err= \frac{\| ref - syn \|}{\sqrt{ \|ref\| \| syn\|}}
      \]
      where ref and syn are vectors.
    - Correlation returns the minimum of the correlation coefficients.

  Args:
    code_name: The name of the code used: specfem2d, specfem3d, specfem3d_globe
    example_name: The name of the example as it appears in the
                  EXAMPLES directory. It can include a directory structure.
                  example: fluid_solid/fluid_solid_external_mesh, Tape2007
    ref_top_dir: The top directory where the reference seismograms are stored.
                 example: /home/buildbot/ExampleReference/
                         and this directory has the structure
                         |__ specfem2d
                         |__ |__ fluid_solid
                         |__ |__ |__ fluid_solid_external_mesh
                         |__ |__ |__ |__ OUTPUT_FILES
                         |__ |__ |__ from_2000_Geophysics_paper_flat_ocean_bottom
                         |__ |__ |__ |__ OUTPUT_FILES
                         |__ |__ |__ from_2000_Geophysics_paper_sinusoidal_ocean_bottom
                         |__ |__ |__ |__ OUTPUT_FILES
                         |__ |__ M2_UPPA
                         |__ |__ |__ OUTPUT_FILES
                         |__ specfem3d
                             |__ homogeneous_halfspace_HEX8_elastic_absorbing_Stacey_5sides
                                 |__ OUTPUT_FILES
    TOL_CORR: The tolerance for the correlation test. TOL_CORR=1 means perfect
              match. TOL_CORR is a global variable.
    TOL_ERR: The tolerance for the least square test. TOL_ERR=0. means perfect
             match.
             TOL_ERR is a global variable.

  Returns:
    Prints the results of the tests to the screen.
    Returns 0 for success, 1 for failure.

  Example:
      CheckExamples.py  specfem2d fluid_solid/fluid_solid_external_mesh \
               /home/buildbot/ExampleReference/

  Assumptions:
    There is a script called "run_this_example.sh" in:
        code_name/EXAMPLES/example_name
      that is used to run the example.
    The seismograms to be checked are in
      code_name/EXAMPLES/example_name/OUTPUT_FILES
    The execution directory is the top level of the repo. e.g. specfem2d, where
      specfem2d is assumed to contain the directory EXAMPLES/example_name
    The seismograms are all the files in OUTPUT_FILES with suffix ".sem*"
  """
  # get input parameters
  #=====================
  res = sys.argv
  code_name=res[1]
  example_name=res[2]
  ref_top_dir=res[3]

  # run the example
  #================
  top_repo_dir=os.getcwd()
  exec_dir='EXAMPLES/' + example_name
  os.chdir(exec_dir)
  rc, ans, errs = run('./run_this_example.sh')
  os.chdir(top_repo_dir)

  # set up reference and examples directories for the comparison
  #=============================================================
  ref_dir= ref_top_dir + '/' + code_name + '/' + \
           example_name  + '/OUTPUT_FILES/'
  example_dir= 'EXAMPLES/' +  example_name + '/OUTPUT_FILES/'

  # compare the seismograms
  #========================
  if CompareAllSeismograms(ref_dir, example_dir):
    print('Success')
    sys.exit(0)
  else:
    print('Failure')
    sys.exit(1)

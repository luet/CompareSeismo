Summary
=======

Runs an example and compare its seismograms with a reference.

Usage
=====

`CheckExamples.py code_name example_name ref_top_dir`

It needs to be called from the top directory of the repository e.g. specfem2d. 
This directory needs to contain the EXAMPLES directory. 

The environment variabes needed to compile the code are given in a module called `env_config.py`. 
This will need to be modified for your system. 

Two measures are used to compare the seismograms:

-   least squares error defined as
    
    ![](https://github.com/luet/CompareSeismo/blob/master/doc/LeastSquare.png)
    
    where ref and syn are vectors.
-   Correlation returns the minimum of the correlation coefficients. The correlation coefficients are defined in the [numpy reference](http://docs.scipy.org/doc/numpy/reference/generated/numpy.corrcoef.html).

For more usage information see the [tutorial in the Wiki](https://github.com/luet/CompareSeismo/wiki/CompareSeismo-Tutorial)
Args
====

-   `code_name`: The name of the code used: specfem2d, specfem3d, specfem3d\_globe
-   `example_name`: The name of the example as it appears in the EXAMPLES directory. It can include a directory structure. example: fluid\_solid/fluid\_solid\_external\_mesh, Tape2007
-   `ref_top_dir`: The top directory where the reference seismograms are stored. 
     example: `/home/buildbot/ExampleReference` and this directory has the structure

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
        |__ |__ homogeneous_halfspace_HEX8_elastic_absorbing_Stacey_5sides
            |__ |__ OUTPUT_FILES

-   `TOL_CORR`: The tolerance for the correlation test. TOL\_CORR=1 means perfect match. TOL\_CORR is a global variable.
-   `TOL_ERR`: The tolerance for the least square test. TOL\_ERR=0. means perfect match.
-   `TOL_ERR` is a global variable.

Returns
=======

Prints the results of the tests to the screen. Returns 0 for success, 1 for failure.

Example
=======

    CheckExamples.py specfem2d fluid_solid/fluid_solid_external_mesh home/buildbot/ExampleReference

Assumptions
===========

There is a script called "run\_this\_example.sh" in: code\_name/EXAMPLES/example\_name that is used to run the example.

The seismograms to be checked are in `code\_name/EXAMPLES/example\_name/OUTPUT\_FILES`

The execution directory is the top level of the repo. e.g. specfem2d, where specfem2d is assumed to contain the directory `EXAMPLES/example_name` 

The seismograms are all the files in `OUTPUT_FILES` with suffix `".sem*"`


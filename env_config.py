""" Environment variables needed for compiling the code.
    Returns: 
      env_dic: A dictionary containing the environment variables needed to 
        compile the code.
        The keys in the dictionary are the environment variables and the 
        values, which are lists, are the definitions of the associated 
        variable.
"""
env_dic={}

env_PATH="/usr/local/openmpi/1.6.3/gcc/x86_64/bin:"
env_PATH+="/home/buildbot/bin:"
env_PATH+="/usr/local/bin:"
env_PATH+="/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/usr/local/cuda/bin"

env_dic["PATH"]=env_PATH

env_LD_LIBRARY_PATH="/usr/local/openmpi/1.6.3/gcc/x86_64/lib64:"
env_LD_LIBRARY_PATH+="/usr/local/lib64/openmpi:"

env_dic["LD_LIBRARY_PATH"]=env_LD_LIBRARY_PATH

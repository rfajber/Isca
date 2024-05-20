import os
import sys
import numpy as np

from isca import GreyCodeBase, DiagTable, Experiment, Namelist, GFDL_BASE

base_dir = os.path.dirname(os.path.realpath(__file__))
# a CodeBase can be a directory on the computer,
# useful for iterative development
cb = GreyCodeBase.from_directory(GFDL_BASE)

# or it can point to a specific git repo and commit id.
# This method should ensure future, independent, reproducibility of results.
# cb = DryCodeBase.from_repo(repo='https://github.com/isca/isca', commit='isca1.1')

# compilation depends on computer specific settings.  The $GFDL_ENV
# environment variable is used to determine which `$GFDL_BASE/src/extra/env` file
# is used to load the correct compilers.  The env file is always loaded from
# $GFDL_BASE and not the checked out git repo.
if len(sys.argv)>1:
    do_clean=sys.argv[1]
    print(do_clean)
    if do_clean == 1:
        os.rmdir('/scratch/rfajber/gfdl_work/codebase/_home_rfajber_Isca/build/grey_isca/')
                  
cb.compile()  # compile the source code to working directory $GFDL_WORK/codebase

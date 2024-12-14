#!/bin/bash
#SBATCH --ntasks=32
#SBATCH --mem-per-cpu=1G
#SBATCH --time=1-00:00
#SBATCH --job-name=FriersonT85
#SBATCH --output=/scratch/rfajber/outerr/%x-%j.out
#SBATCH --error=/scratch/rfajber/outerr/%x-%j.err
#SBATCH --account=def-rfajber

#not sure if this is needed but just in case 
# directory of the Isca source code
export GFDL_BASE=/home/rfajber/Isca 
# &quot;environment&quot; configuration for emps-gv4
export GFDL_ENV=narval.ifort
# temporary working directory used in running the model
export GFDL_WORK=/scratch/rfajber/gfdl_work
# directory for storing model output
export GFDL_DATA=/scratch/rfajber/gfdl_data

#conda init bash
#conda activate isca_env

source /home/rfajber/.bashrc 
conda activate isca_env

cd $GFDL_BASE/exp/test_cases/frierson

python frierson_test_case.py
#!/bin/bash
#SBATCH --ntasks=32
#SBATCH --mem-per-cpu=2G
#SBATCH --time=1-00:00
#SBATCH --job-name=FriersonWTagsT85
#SBATCH --error=/scratch/rfajber/outerr/%x-%j.err
#SBATCH --output=/scratch/rfajber/outerr/%x-%j.out
#SBATCH --account=ctb-cdufour

source /home/rfajber/.bashrc 
conda activate isca_env

cd $GFDL_BASE/exp/RF

python GreyInput.py --expname WTagsX4 --hroutput 1 --maxrun 120 --NCORES 32 --debugoutput 1 --resolution T42
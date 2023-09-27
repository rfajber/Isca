#!/bin/bash
#SBATCH --ntasks=16
#SBATCH --mem-per-cpu=3500M
#SBATCH --time=1-00:00
#SBATCH --job-name=FriersonWTagsT
#SBATCH --output=/scratch/rfajber/outerr/%x-%j.out
#SBATCH --error=/scratch/rfajber/outerr/%x-%j.err
#SBATCH --account=def-rfajber

source /home/rfajber/.bashrc 
conda activate isca_env

cd $GFDL_BASE/exp/RF

python frierson_test_case_water_tags.py
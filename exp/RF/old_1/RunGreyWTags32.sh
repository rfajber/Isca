#!/bin/bash
#SBATCH --ntasks=64
#SBATCH --mem-per-cpu=2G
#SBATCH --time=1-00:00
#SBATCH --job-name=FriersonWTagsT85
#SBATCH --error=/scratch/rfajber/outerr/%x-%j.err
#SBATCH --output=/scratch/rfajber/outerr/%x-%j.out
#SBATCH --account=def-rfajber

source /home/rfajber/.bashrc 
conda activate isca_env

cd $GFDL_BASE/exp/RF

python GreyT8532_1.py
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --mem=0
#SBATCH --time=1-00:00
#SBATCH --job-name=FriersonWTagsT85
#SBATCH --error=/scratch/rfajber/outerr/%x-%j.err
#SBATCH --output=/scratch/rfajber/outerr/%x-%j.out
#SBATCH --account=def-rfajber

source /home/rfajber/.bashrc 
conda activate isca_env

cd $GFDL_BASE/exp/RF

python GreyT8564.py
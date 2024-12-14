#!/bin/bash
#SBATCH --ntasks=32
#SBATCH --mem-per-cpu=2G
#SBATCH --time=0-04:00
#SBATCH --job-name=HS_parameter_sweep
#SBATCH --error=/scratch/rfajber/outerr/%x-%j.err
#SBATCH --account=def-rfajber

source /home/rfajber/.bashrc 
conda activate isca_env

cd $GFDL_BASE/exp/RF

python parameter_sweep.py

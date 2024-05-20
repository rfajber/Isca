#!/bin/bash
#SBATCH --ntasks=32
#SBATCH --mem-per-cpu=2G
#SBATCH --time=2-00:00
#SBATCH --job-name=E2
#SBATCH --error=/scratch/rfajber/outerr/%x-%j.err
#SBATCH --account=ctb-cdufour

source /home/rfajber/.bashrc 
conda activate isca_env

cd $GFDL_BASE/exp/RF

python GreyInput.py --expname WTagsGB0_E2 --qflux_amp 60.0 

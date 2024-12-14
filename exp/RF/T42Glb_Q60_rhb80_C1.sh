#!/bin/bash
#SBATCH --ntasks=32
#SBATCH --mem-per-cpu=2G
#SBATCH --time=1-00:00
#SBATCH --job-name=Q60_rhb80_C1
#SBATCH --error=/scratch/rfajber/outerr/%x-%j.err
#SBATCH --account=ctb-cdufour

source /home/rfajber/.bashrc 
conda activate isca_env

cd $GFDL_BASE/exp/RF

python GreyInput.py --expname T42Glb_Q60_rhb80_C1 --qflux 60.0

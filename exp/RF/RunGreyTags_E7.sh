#!/bin/bash
#SBATCH --ntasks=64
#SBATCH --mem-per-cpu=2G
#SBATCH --time=2-00:00
#SBATCH --job-name=E7
#SBATCH --error=/scratch/rfajber/outerr/%x-%j.err
#SBATCH --account=def-rfajber

source /home/rfajber/.bashrc 
conda activate isca_env

cd $GFDL_BASE/exp/RF

python GreyInput.py --expname WTagsNH_E7 --restart_file WTagsNHctrl.1800.tar.gz --carbon_conc 720.0
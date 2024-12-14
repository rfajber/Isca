#!/bin/bash
#SBATCH --ntasks=64
#SBATCH --mem-per-cpu=2G
#SBATCH --time=2-00:00
#SBATCH --job-name=E11
#SBATCH --error=/scratch/rfajber/outerr/%x-%j.err
#SBATCH --account=def-rfajber

source /home/rfajber/.bashrc
conda activate isca_env

cd $GFDL_BASE/exp/RF

python GreyInput.py --expname WTagsNH_E11 --restart_file WTagsNHctrl.1800.tar.gz --qflux_amp 60.0 --do_seasonal 1 --maxrun 192

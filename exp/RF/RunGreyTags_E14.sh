#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --mem=0
#SBATCH --time=2-00:00
#SBATCH --job-name=E14
#SBATCH --error=/scratch/rfajber/outerr/%x-%j.err
#SBATCH --account=ctb-cdufour

source /home/rfajber/.bashrc
conda activate isca_env

cd $GFDL_BASE/exp/RF

python GreyInput.py --expname WTagsNH_E14 --restart_file WTagsNHctrl.1800.tar.gz --do_seasonal 1 --maxrun 192 --carbon_conc 720.0

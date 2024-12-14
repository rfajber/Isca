#!/bin/bash
#SBATCH --ntasks=32
#SBATCH --mem-per-cpu=2G
#SBATCH --time=0-02:00
#SBATCH --job-name=Q00_rhb80_C1
#SBATCH --error=/scratch/rfajber/outerr/%x-%j.err
#SBATCH --account=ctb-cdufour

source /home/rfajber/.bashrc 
conda activate isca_env

cd $GFDL_BASE/exp/RF

python GreyInput.py --expname A8 --restart_file t42_test_restart.tar.gz #T42Glb_Q00_rhb80_C1

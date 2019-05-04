#!/bin/bash
#SBATCH --account=def-pjk
#SBATCH --ntasks=8               # number of MPI processes
#SBATCH --job-name=rfht
#SBATCH --output=out/%x-%j.out
#SBATCH --mem-per-cpu=4000M      # memory; default unit is megabytes
#SBATCH --time=01-00:00           # time (DD-HH:MM)
#SBATCH --constraint=broadwell

source /home/rfajber/Isca/isca_env/bin/activate

cd /home/rfajber/Isca/exp/run_isca

python rfht_input_restart.py input_spinup_restart





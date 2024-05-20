#!/bin/bash
#!/bin/bash 
#SBATCH --ntasks=32
#SBATCH --mem-per-cpu=3500M
#SBATCH --time=0-10:00
#SBATCH --job-name=FriersonWTagsT85
#SBATCH --error=/scratch/rfajber/outerr/%x-%j.err
#SBATCH --account=def-rfajber

source /home/rfajber/.bashrc 
conda activate isca_env

cd $GFDL_BASE/exp/RF

python frierson_test_case_water_tags_32_qflux.py

#!/bin/bash
#!/bin/bash 
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --mem=0
#SBATCH --time=1-00:00
#SBATCH --job-name=FriersonWTagsT
#SBATCH --output=/scratch/rfajber/outerr/%x-%j.out
#SBATCH --error=/scratch/rfajber/outerr/%x-%j.err
#SBATCH --account=def-rfajber

source /home/rfajber/.bashrc 
conda activate isca_env

cd $GFDL_BASE/exp/RF

python frierson_test_case_water_tags_64.py
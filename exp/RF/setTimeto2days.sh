#!/bin/bash

for i in $(seq 0 10); do

#sed -i '/#SBATCH --time=1-00:00/c\#SBATCH --time=2-00:00' RunGreyTags_E$i.sh
sed -i '/#SBATCH ---account=def-rfajber/c\#SBATCH --account=ctb-cdufour' RunGreyTags_E$i.sh

done 
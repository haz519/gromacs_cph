#!/bin/csh
#SBATCH --partition=im1080-gpu
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=12
#SBATCH --export=ALL
#SBATCH -t 48:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=haz519@lehigh.edu

#source /usr/local/gromacs_constantph/bin/GMXRC
source /etc/profile.d/zlmod.sh

module load cuda/11.6.0
module load mpich/3.3.2
module load numpy
module load python

/share/ceph/woi216group-c2/shared/share_dos221/gromacs/constantph/gromacs-constantph/build/bin/gmx grompp -f MD.mdp -c equilibrated.pdb -p topol.top -n index.ndx -o MD.tpr
/share/ceph/woi216group-c2/shared/share_dos221/gromacs/constantph/gromacs-constantph/build/bin/gmx mdrun -v -deffnm MD -npme 0

#gmx cphmd -s MD.tpr -e MD.edr -numplot 1

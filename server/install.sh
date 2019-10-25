#!/bin/bash

ENV_NAME=ml-web-demo

# create environment
if ! conda env create --file environment.yml --name ${ENV_NAME}
then
  exit
fi

source ~/anaconda3/etc/profile.d/conda.sh
conda activate ${ENV_NAME}

python_base=~/anaconda3/envs/${ENV_NAME}/lib/python3.7
cd ${python_base} || exit
# fix _gdbm module not found error
sed -i '1 ! s/_gdbm/dbm/' dbm/gnu.py

# Review prediction model service
## Install
```shell script
conda env create -f environment.yml
conda activate ntu-nlp-review

# copy repository
cp -r ../core third

# create structure
mkdir -p app/weight
```
## Download Weights

## Deployment
```shell script
cd app || return 1
sh run-server.sh
```

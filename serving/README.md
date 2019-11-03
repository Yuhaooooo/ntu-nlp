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
Download [weights](https://drive.google.com/open?id=1QHTaTORNstkfrCJDRvQ3g0iz52wgEjk_), move and unzip it under `app`
using:
```shell script
tar xvzf weights.tar.gz
```

## Deployment
```shell script
cd app || return 1
sh run-server.sh
```

# CZ4045_Natural_Language_Processing

## Install

#### Option 1. Step-by-step Installation
Please make sure that you have installed Conda.
```shell script
# install Conda env
conda env create -f environment.yml
# activate Conda env
conda activate ntu-nlp

# create data folders
mkdir -p core/data
```

## Download Data

#### Option 1. Auto-script
```shell script
sh scripts/download-data.sh
```

#### Option 2. Step-by-step download
1. Download [preprocessed data](https://drive.google.com/open?id=1ay53rIluB334-RUqn28GR-QI6HxutJ6H) and move it into `core/data`.

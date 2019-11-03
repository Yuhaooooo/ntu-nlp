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
mkdir -p core/{data,output}

# Download model
python -m spacy download en
python -c 'import nltk; nltk.download('vader_lexicon')'
```

## Download Data

#### Option 1. Auto-script
```shell script
sh scripts/download-data.sh
```

#### Option 2. Step-by-step download
1. Download [preprocessed data](https://drive.google.com/open?id=1pkvBtO7B8suZx-tYttlUNcCoP4WPsWLr), move it into `core/data`
and unzip:
```shell script
tar xvzf data.tar.gz
```

## Demo
#### Run Web Application
You have to run three microservices in `serving`, `server`, and `web-app`. See 
[Model server instruction](serving/README.md), [API server instruction](server/README.md) and [frontend instruction](web-app/README.md).

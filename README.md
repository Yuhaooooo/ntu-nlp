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

## 3.2 Data Analysis
#### Writing Style
```shell script
python 
```
#### Sentence Segmentation
```shell script
python 
```
#### Tokenization and Stemming
```shell script
python 
```
#### POS Tagging
```shell script
python 
```
#### Most Frequent Adjectives for each Rating
```shell script
python 
```

## 3.3 Noun Adjective Pair Summarizer
#### Rule based method: POS Tagging + FSA
```shell script
python core/examples/3.3 Adj-Noun Pairs/Adj_Noun_Pairs.py 
```
You can change these variables:
numberOfBusinessId=5 [line 11, int, the number of different business id]
numberOfPairs=5 [line 12, int, the number of noun-adj pairs for each business id]
withExtra=False [line 13, boolean, if the extra wolds included, eg. good / very good]
The generated dataframe will be stored in core/examples/3.3 Adj-Noun Pairs/Adj_Noun_Pairs.csv
#### Bert-based method: 
```shell script
python 
```

## 3.4 Application




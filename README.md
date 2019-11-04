

# CZ4045_Natural_Language_Processing

**Please run all the commands in the directory `ntu-nlp/`**

## Install

Please make sure that you have installed Conda.
```shell script
# install Conda env
conda env create -f environment.yml
# activate Conda env
conda activate ntu-nlp

# create data folders
mkdir -p core/{data,output}

# Download packages
python -m spacy download en
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')"
```

## Prepare Data
#### Three csv files are needed for this project: 
* data.csv (task 3.2, 3.3 and 3.4)
* train.csv (task 3.3 Bert-model and 3.4)
* val.csv (task 3.3 Bert-model and 3.4) 

	
### Step 1: Download Data

#### Option 1 Auto-script
```shell script
sh scripts/download-data.sh
```


#### Option 2. Step-by-step download
1. Download [data](https://drive.google.com/open?id=1Xu-BAztca_HduVoU2h-LcQpfI1gcau0Q), move it into `core/data/`
and unzip:
```shell script
cd core/data
unzip data.zip
```

### Step 2: Data Process
```shell script
python core/examples/data_preprocess.py core/data/reviewSelected100.json
```
**Note**:  
1. You need to give the correct absolute path of the Json data file. 
2. Input: data file in Json.
3. Output: `core/data/{data, train, val}.csv`, which serves tasks after

## Execution
### 3.2 Data Analysis

#### Sentence Segmentation
```shell script
python core/examples/3.2-Dataset-analysis/sentence_segmentation.py
```
**Note**:  
1. Input: `core/data/data.csv`  
2. Output: `core/examples/3.2-Dataset-analysis/results/sentence_segmentation_by_star/`  
3. Once sentence segmentation for a rating star is completed, the corresponding plot of review counts VS sentence counts will be displayed. For now, plots are displayed one by one. To view the plot for the next rating star, close the current plot. To save the image, click the "save" icon at the bottom of the plot display.


#### Tokenization and Stemming
```shell script
python core/examples/3.2-Dataset-analysis/tokenization_stemming.py
```
**Note**:  
1. Input: `core/data/data.csv` <br/>
2. Output: `core/examples/3.2-Dataset-analysis/results/tokenize_and_stemming/`, `core/examples/3.2-Dataset-analysis/results/top_20_words/` <br/>
3. Once tokenization is completed, the corresponding plot of review counts VS token counts will be displayed. For now, plots are displayed one by one. To view the next plot, close the current plot. To save the image, click the "save" icon at the bottom of the plot display.  <br/>
4. You may modify the argument in get_most_freq(num=20) to view any number of most frequent tokens <br/>


#### POS Tagging
```shell script
python core/examples/3.2-Dataset-analysis/pos_tag.py 
```
**Note**:
1. Input: `core/data/data.csv` <br/>
2. Output: `core/examples/3.2-Dataset-analysis/results/pos_tagging/tagger_result.csv`
    The CSV file contains five sections: each section includes the tagging results produced by a different tagger for the same sentence. The order of taggers which generate the results are: default tagger, regex-based tagger, baseline tagger, unigram tagger, unigram tagger with backoff, bigram tagger, bigram tagger with backoff, trigram tagger, trigram tagger with backoff and perceptron tagger. <br/>
3. The random seed is set to be 22, so that it will produce the same output every time. Change the seed if you wish to get different output.  <br/>


#### Most Frequent Adjectives for each Rating

```shell script
python core/examples/3.2-Dataset-analysis/most_freq_adj.py
```

**Note**:
1. Input: `core/data/data.csv`  <br/>
2. Output: `core/examples/3.2-Dataset-analysis/results/most_freq_adj/` <br/>
3. The script will first group the reviews based on the rating star and generate a csv for each rating star (e.g. r1_review.csv). Afterwards, the most frequent words are counted and the results are stored in most_freq_adj.csv. Lastly, the most indicative words are calculated and the results are stored in most_indicative_adj.csv.   <br/>

### 3.3 Noun Adjective Pair Summarizer
#### Rule based method: POS Tagging + FSA
```shell script
python core/examples/3.3-Adj-Noun-Pairs/adj_noun_extractor1.py  
``` 

**Note**:
1. Input: `core/data/data.csv`  <br/>
2. Output: `core/examples/3.3-Adj-Noun-Pairs/adj_noun_pairs1.csv` <br/>
3. numberOfBusinessId=5 [line 11, int, the number of different business id] <br/>
numberOfPairs=5 [line 12, int, the number of noun-adj pairs for each business id] <br/>
withExtra=False [line 13, boolean, if the extra wolds included, eg. good / very good] <br/>

#### Bert-based method: 
```shell script
python core/examples/3.3-Adj-Noun-Pairs/adj_noun_extractor2.py 
```
**Note**:
1. Input: `core/data/data.csv`  <br/>
2. Output: the noun-adj pairs extracted printed out in the order of the business ids. <br/>

### 3.4 Application
#### Sentiment analysis
```shell script
python core/examples/3.4-sentiment-analysis/sentiment_analysis.py
```
#### RNN model
Train:  
```shell script
export PYTHONPATH="${PWD}/core"
python core/examples/3.4-sentiment-analysis/sentiment_analysis_train.py
unset PYTHONPATH
```
Predict:  
Change inputs here:
```
...
    input_list=[[
        "Appreciate the call ahead seating! Always a joy to go in n sit down with in 15 mins MAX! Thanks for awesome food and service!"
    ], ["delicious, grubby, chinese food in generous portions and always great service. their szchewaun chicken is THE BOMB. so spicy it makes me sweat."]],
...
```
And run:
```shell script
export PYTHONPATH="${PWD}/core"
python core/examples/3.4-sentiment-analysis/sentiment_analysis_predict.py
unset PYTHONPATH
```
**Note**:
1. Input: a text string <br/>
2. Output: the degree of sentiment analyzed. <br/>

#### Run Web Application
You have to run three microservices in `serving`, `server`, and `web-app`. See 
[Model server instruction](serving/README.md), [API server instruction](server/README.md) and [frontend instruction](web-app/README.md).

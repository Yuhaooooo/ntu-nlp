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
python3
```
#### Sentence Segmentation
```shell script
python3
```
#### Tokenization and Stemming
```shell script
python3 
```
#### POS Tagging
```shell script
python3 core/examples/3.2-Dataset-analysis/pos_tag.py 
```
Note: <br/>
1. You need to edit the pos_tag.py file so that the csv_file_path in the main() is correctly pointing to the data.csv you downloaded.  <br/>
    ```python
    def main():  
        csv_file_path = join('..', "data.csv")  
      
        pos_tagger = POSTagger(csv_file_path)  
        pos_tagger.tag_random_sentences(5) 
```
2. The random seed is set to be 22, so that it will produce the same output every time. Comment out the seed if you wish to get different output.  <br/>
3. The output is stored in ./core/examples/3.2-Dataset-analysis/results/pos_tagging/tagger_result.csv. The CSV file contains five sections: each section includes the tagging results produced by a different tagger for the same sentence. The order of taggers which generate the results are: default tagger, regex-based tagger, baseline tagger, unigram tagger, unigram tagger with backoff, bigram tagger, bigram tagger with backoff, trigram tagger, trigram tagger with backoff and perceptron tagger.  <br/>


#### Most Frequent Adjectives for each Rating
```shell script
python3 core/examples/3.2-Dataset-analysis/most_freq_adj.py
```
Note: <br/>
1. You need to edit the pos_tag.py file so that the csv_file_path in the main() is correctly pointing to the data.csv you downloaded.  <br/>
    ```python
    if __name__ == "__main__":  
        reviews_separated = False  
        most_freq_adj = False  
        most_indicative_adj = False  
      
        csv_file_path = join('..', "data.csv")  
        output_path = join(getcwd(), "results", "most_freq_adj")  
      
        adjExtractor = AdjExtractor(csv_file_path, output_path)  
```
2. The output is saved in ./core/examples/3.2-Dataset-analysis/results/most_freq_adj/.   <br/>
3. The script will first group the reviews based on the rating star and generate a csv for each rating star (e.g. r1_review.csv). Afterwards, the most frequent words are counted and the results are stored in most_freq_adj.csv. Lastly, the most indicative words are calculated and the results are stored in most_indicative_adj.csv.  <br/>

## 3.3 Noun Adjective Pair Summarizer
#### Rule based method: POS Tagging + FSA
```shell script
python3 core/examples/3.3 Adj-Noun Pairs/Adj_Noun_Pairs.py 
``` 
Note: <br/>
1. You can change these variables: <br/>
    numberOfBusinessId=5 [line 11, int, the number of different business id] <br/>
    numberOfPairs=5 [line 12, int, the number of noun-adj pairs for each business id] <br/>
    withExtra=False [line 13, boolean, if the extra wolds included, eg. good / very good] <br/>
2. The generated dataframe will be stored in core/examples/3.3 Adj-Noun Pairs/Adj_Noun_Pairs.csv <br/>
#### Bert-based method: 
```shell script
python 
```

## 3.4 Application




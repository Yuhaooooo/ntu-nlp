import json
import pylab as plt
import nltk
import numpy as np
from os import getcwd
import pandas as pd
from os.path import join

ps = nltk.stem.PorterStemmer()
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')


## return a list of tokens for the given review

def tokenize(review):
	return tokenizer.tokenize(review)


## for the given list of tokens
## convert all tokens to lower case
## filter out the stop words

def apply_filter(tokens):
	default_stopwords = set(nltk.corpus.stopwords.words('english'))
	tokens = [token.lower() for token in tokens]
	tokens = [token for token in tokens if token not in default_stopwords]
	return tokens
	

## return a list of token lists
## if merge_all, return a list of all tokens
## apply stemming and filter as indicated

def all_tokenized(data, stemming=False, merge_all=False, filter=False):
	tokens_list = []
	for i in range(len(data)):
		tokens = tokenize(data["text"][i])
		if apply_filter:
			tokens = apply_filter(tokens)

		if merge_all: ## do not group tokens by review
			if stemming:
				stem_tokens = [ps.stem(token) for token in tokens]
				tokens_list += stem_tokens
			else:
				tokens_list += tokens
		else:
			if stemming:
				stem_tokens = [ps.stem(token) for token in tokens]
				tokens_list.append(stem_tokens)
			else:
				tokens_list.append(tokens)	
	return tokens_list


## return the lengths of each token list
## in the given list of token lists

def lens(tokens_list):
	counts = []
	for tokens in tokens_list:
		counts.append(len(tokens))
	return counts


## return the number of reviews of each token count

def counts_per_len(counts):
	counts_cnt = []
	counts.sort()
	for i in range(counts[-1]+1):
		counts_cnt.append(0)

	for element in counts:
		counts_cnt[element] +=1

	return counts_cnt


## Plot the review count VS token count figure'

def plot(data, index, label):
	plt.figure(index)
	plt.bar(np.arange(len(data)), data, align='center', label=label)
	plt.xlabel('Token Count')
	plt.ylabel('Review Count')
	plt.legend()
	plt.show()


## main program for Q3.2 Task 3 Part 1

def run():
	csv_path = join('..', '..', 'data', "data.csv")
	data = pd.read_csv(csv_path)

	all_tokens =all_tokenized(data, stemming=False, merge_all=False)
	all_lens = lens(all_tokens)
	counts_cnt = counts_per_len(all_lens)
	plot(counts_cnt, index=1, label="without stemming")

	all_tokens_stemmed =all_tokenized(data, stemming=True)
	all_lens_stemmed = lens(all_tokens_stemmed)
	counts_cnt_stemmed = counts_per_len(all_lens_stemmed)
	plot(counts_cnt_stemmed, index=2, label="with stemming")


## returns a frequency dictionary for the given tokens

def get_dict(all_tokens):
	freq_dict = nltk.FreqDist(all_tokens)
	return freq_dict


## print the top n tokens

def print_top_results(freq_dict, num):
	for word, frequency in freq_dict.most_common(num):
		print(u'{}: {}'.format(word, frequency))
	print("\n")


## main program for Q3.2 Task 3 Part 2

def get_most_freq(num=20):
	
	csv_path = join('..', '..', 'data', "data.csv")
	data = pd.read_csv(csv_path)

	all_tokens =all_tokenized(data, stemming=False, merge_all=True, filter=True)
	freq_dict = get_dict(all_tokens)

	all_tokens_stemmed = all_tokenized(data, stemming=True, merge_all=True, filter=True)
	freq_dict_stemmed = get_dict(all_tokens_stemmed)

	print("Top {} words without stemming: \n".format(num))
	print_top_results(freq_dict, num)
	print("Top {} words with stemming: \n".format(num))
	print_top_results(freq_dict_stemmed, num)



if __name__ == "__main__":
	run()
	get_most_freq(20)



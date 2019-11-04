import json
import pylab as plt
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
import numpy as np
from os import getcwd
import pandas as pd
from os.path import join

tokenizer = PunktSentenceTokenizer()


## categorize reviews by star
## return a 2-D list of reviews
## list at order_by_star[i] contains reviews with (i+1) stars

def by_star(data, star=5):
	order_by_star = []
	for i in range(star):
		order_by_star.append([])

	for i in range(len(data)):
		star = int(data["stars"][i])
		order_by_star[star-1].append(data["text"][i])

	return order_by_star


## pass in a single review
## return the counts of segments/sentences

def segment(review):
	global tokenizer
	sentences = tokenizer.tokenize(review)
	#print(sentences)
	return len(sentences)


## return a list of sentence counts
## for each review in the given review list

def lens(review_list):
	counts = []
	for review in review_list:
		count = segment(review)
		counts.append(count)
	return counts


## return the number of reviews for each sentence count

def counts_per_len(counts):
	counts_cnt = []
	counts.sort()
	for i in range(counts[-1]+1):
		counts_cnt.append(0)

	for element in counts:
		counts_cnt[element] +=1

	return counts_cnt


## plot the review count vs sentence count for each star

def plot(data, index):
	plt.figure(index)
	plt.bar(np.arange(len(data)), data, align='center', alpha=0.5, label="Rating Star = " + str(index))
	plt.xlabel('Sentence Count')
	plt.ylabel('Review Count')
	plt.legend()
	plt.show()


## main program for Q3.2 part 2

def run():
	csv_path = join(getcwd(), 'core', 'data', 'data.csv')
	data = pd.read_csv(csv_path)
	order_by_star = by_star(data, star=5)

	for i, per_star in enumerate(order_by_star):
		all_lens = lens(per_star)
		counts_cnt = counts_per_len(all_lens)
		plot(counts_cnt, index=i+1)


if __name__ == "__main__":
	run()
	'''
	source = "Awesome and home made fresh breads .... congrats move to corner store and look great and more room for customer"
	n = segment(source)
	print(n)
	'''


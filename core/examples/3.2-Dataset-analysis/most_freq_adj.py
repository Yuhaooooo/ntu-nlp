import nltk
from nltk import word_tokenize, pos_tag
import pandas as pd
from os.path import join, exists
from os import getcwd, makedirs
import csv
from tqdm import tqdm
from math import log

class AdjExtractor:

    def __init__(self, csv_path, output_path):
        self.data = pd.read_csv(csv_path, index_col=[0])
        self.output_path = output_path
        self.size = len(self.data)
        self.r1_review_path = join(self.output_path, 'r1_reviews.csv')
        self.r2_review_path = join(self.output_path, 'r2_reviews.csv')
        self.r3_review_path = join(self.output_path, 'r3_reviews.csv')
        self.r4_review_path = join(self.output_path, 'r4_reviews.csv')
        self.r5_review_path = join(self.output_path, 'r5_reviews.csv')

        if not exists(self.output_path):
            makedirs(self.output_path)


    def group_reviews_by_rating(self):
        r1_writer = csv.writer(open(self.r1_review_path, 'w'), delimiter=',')
        r2_writer = csv.writer(open(self.r2_review_path, 'w'), delimiter=',')
        r3_writer = csv.writer(open(self.r3_review_path, 'w'), delimiter=',')
        r4_writer = csv.writer(open(self.r4_review_path, 'w'), delimiter=',')
        r5_writer = csv.writer(open(self.r5_review_path, 'w'), delimiter=',')

        writer_list = [
            r1_writer,
            r2_writer,
            r3_writer,
            r4_writer,
            r5_writer
        ]

        for writer in writer_list:
            writer.writerow(["rating", "review"])

        print("----- Starting separting reviews by rating star, output directory: {}".format(self.output_path))
        for i in tqdm(range(self.size)):
            star = int(self.data['stars'][i])
            review = self.data['text'][i]
            mapping[star-1].writerow([star, review])

    def extract_top_ten_most_freq_adj(self):

        f = open(join(self.output_path, "most_freq_adj.csv"), 'w')
        f_writer = csv.writer(f)
        f_writer.writerow(["star", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        reviews_list = [
            self.r1_review_path,
            self.r2_review_path,
            self.r3_review_path,
            self.r4_review_path,
            self.r5_review_path
        ]

        for i in range(len(reviews_list)):
            reviews = pd.read_csv(reviews_list[i])['review']
            size = len(reviews)

            fd = nltk.FreqDist()

            print("----- Extracting top-10 most frequent adjectives for rating star {}".format(i+1))

            for j in tqdm(range(size)):
                for (word, tag) in pos_tag(word_tokenize(reviews[j])):
                    if tag == "JJ":
                        fd[word.lower()] += 1

            f_writer.writerow([i+1] + fd.most_common(10))

        f.close()

    def extract_top_ten_most_indicative_adj(self):

        reviews_list = [
            self.r1_review_path,
            self.r2_review_path,
            self.r3_review_path,
            self.r4_review_path,
            self.r5_review_path
        ]

        f = open(join(self.output_path, "most_indicative_adj.csv"), 'w')
        f_writer = csv.writer(f)
        f_writer.writerow(["star", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

        total_fd = nltk.FreqDist()
        total_num_tokens = 0

        fd_by_rating = []
        num_tokens_by_rating = []

        print("----- Extracting top-10 most indicative adjectives for all rating stars")

        for path in reviews_list:
            reviews = pd.read_csv(path)['review']
            size = len(reviews)
            count = 0
            current_fd = nltk.FreqDist()

            for i in tqdm(range(size)):
                for (word, tag) in pos_tag(word_tokenize(reviews[i])):
                    if word.lower().isalpha():
                        count += 1

                    if tag == "JJ":
                        current_fd[word.lower()] += 1
                        total_fd[word.lower()] += 1

            fd_by_rating.append(current_fd)
            num_tokens_by_rating.append(count)

            total_num_tokens += count

        for i in range(len(reviews_list)):
            prob = {}

            for word in fd_by_rating[i]:
                p_w_given_r = fd_by_rating[i][word] / num_tokens_by_rating[i]

                total_occurance_of_word = 0

                for fd in fd_by_rating:
                    total_occurance_of_word += fd[word]

                p_w = total_occurance_of_word / total_num_tokens

                prob[word] = p_w_given_r * log(p_w_given_r / p_w)

            sorted_prob = sorted(prob.items(), key=lambda kv : kv[1])

            f_writer.writerow([i+1] + sorted_prob[-1: -11: -1])

        f.close()


if __name__ == "__main__":
    reviews_separated = False
    most_freq_adj = False
    most_indicative_adj = False

    csv_file_path = join('..', "data.csv")
    output_path = join(getcwd(), "results", "most_freq_adj")

    adjExtractor = AdjExtractor(csv_file_path, output_path)

    if not reviews_separated:
        adjExtractor.group_reviews_by_rating()

    if not most_freq_adj:
        adjExtractor.extract_top_ten_most_freq_adj()

    if not most_indicative_adj:
        adjExtractor.extract_top_ten_most_indicative_adj()



import nltk
from nltk.corpus import brown
import random
import pandas as pd
from os.path import join, dirname, realpath
from os import getcwd
import csv

class POSTagger:

    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path)
        self.size = len(self.data)
        self.init_nltk()
        self._init_all_tagger()
        random.seed(22)
        

    def init_nltk(self):
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')

    def _init_all_tagger(self):
        print("----- Initializing taggers")
        self._init_default_tagger()
        self._init_regex_tagger()
        self._init_baseline_tagger()
        self._init_unigram_tagger()
        self._init_bigram_tagger()
        self._init_trigram_tagger()
        print("----- Initialization done\n")

    def _init_default_tagger(self):
        # get the most frequent tag in brown corpus
        brown_tagged_words = brown.tagged_words()

        tags = [tag for (word, tag) in brown_tagged_words]
        most_freq_tag = nltk.FreqDist(tags).max()

        self.default_tagger = nltk.DefaultTagger(most_freq_tag)

    def _init_regex_tagger(self):
        patterns = [
            (r'.*ing$', 'VBG'),
            (r'.*ed$', 'VBD'),
            (r'.*es$', 'VBZ'),
            (r'.*ould$', 'MD'),
            (r'.*\'s$', 'NN$'),
            (r'.*s$', 'NNS'),
            (r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
            (r'.*', 'NN')
        ]

        self.regex_tagger = nltk.RegexpTagger(patterns)

    def _init_baseline_tagger(self):
        brown_tagged_words = brown.tagged_words()
        brown_words = brown.words()

        fd = nltk.FreqDist(brown_words)
        cfd = nltk.ConditionalFreqDist(brown_tagged_words)
        most_freq_words = fd.most_common()[:100]
        likely_tags = dict((word, cfd[word].max()) for (word, freq) in most_freq_words)
        self.baseline_tagger = nltk.UnigramTagger(model=likely_tags)

    def _init_unigram_tagger(self):
        self.unigram_tagger = nltk.UnigramTagger(brown.tagged_sents())
        self.unigram_tagger_with_backoff = nltk.UnigramTagger(brown.tagged_sents(), backoff=self.default_tagger)

    def _init_bigram_tagger(self):
        self.bigram_tagger = nltk.BigramTagger(brown.tagged_sents())
        self.bigram_tagger_with_backoff = nltk.BigramTagger(brown.tagged_sents(), backoff=self.unigram_tagger_with_backoff)

    def _init_trigram_tagger(self):
        self.trigram_tagger = nltk.TrigramTagger(brown.tagged_sents())
        self.trigram_tagger_with_backoff = nltk.TrigramTagger(brown.tagged_sents(), backoff=self.bigram_tagger_with_backoff)

    def tag_with_default_tagger(self, tokens):
        # use default tagger which sets all tags to NN

        return self.default_tagger.tag(tokens)

    def tag_with_regex_tagger(self, tokens):
        # use regex tagger

        return self.regex_tagger.tag(tokens)

    def tag_with_baseline_tagger(self, tokens):
        # use baseline tagger

        return self.baseline_tagger.tag(tokens)

    def tag_with_unigram_tagger(self, tokens, backoff=False):
        # use unigram tagger
        if backoff:
            return self.unigram_tagger_with_backoff.tag(tokens)
        else:
            return self.unigram_tagger.tag(tokens)

    def tag_with_bigram_tagger(self, tokens, backoff=False):
        if backoff:
            return self.bigram_tagger_with_backoff.tag(tokens)
        else:
            return self.bigram_tagger.tag(tokens)

    def tag_with_trigram_tagger(self, tokens, backoff=False):
        if backoff:
            return self.trigram_tagger_with_backoff.tag(tokens)
        else:
            return self.bigram_tagger.tag(tokens)

    def tag_with_perceptron_tagger(self, tokens):
        # using the pre-trained PerceptronTagger model
        # trained on Sections 00-18 of the Wall Street Journal sections of OntoNotes 5
        return nltk.pos_tag(tokens) #, tagset='universal')

    def test(self):
        sentence = self.data['text'][0]
        tokens = nltk.word_tokenize(sentence)

        # testing
        self.tag_with_default_tagger(tokens)
        print("----- Default tagger pass the test")

        self.tag_with_regex_tagger(tokens)
        print("----- Regex tagger pass the test")

        self.tag_with_baseline_tagger(tokens)
        print("----- Baseline tagger pass the test")

        self.tag_with_unigram_tagger(tokens)
        print("----- Unigram tagger pass the test")

        self.tag_with_unigram_tagger(tokens, backoff=True)
        print("----- Unigram tagger with backoff pass the test")

        self.tag_with_bigram_tagger(tokens)
        print("----- Bigram tagger pass the test")

        self.tag_with_bigram_tagger(tokens, backoff=True)
        print("----- Bigram tagger with backoff pass the test")

        self.tag_with_trigram_tagger(tokens)
        print("----- Trigram tagger pass the test")

        self.tag_with_trigram_tagger(tokens, backoff=True)
        print("----- Trigram tagger with backoff pass the test")

        self.tag_with_perceptron_tagger(tokens)
        print("----- Perceptron tagger pass the test")

        print("----- All taggers pass the test\n")


    def tag_random_sentences(self, n, output_path):
        index_list = random.sample(range(0, self.size), n)
        with open(join(output_path, 'tagger_result.csv'), mode='w') as f:
            result_writer = csv.writer(f, delimiter=',')

            print("----- Starting POS tagging\n")

            for index in index_list:
                tokens = nltk.word_tokenize(self.data['text'][index])
                result_writer.writerow(self.tag_with_default_tagger(tokens))
                result_writer.writerow(self.tag_with_regex_tagger(tokens))
                result_writer.writerow(self.tag_with_baseline_tagger(tokens))
                result_writer.writerow(self.tag_with_unigram_tagger(tokens))
                result_writer.writerow(self.tag_with_unigram_tagger(tokens, backoff=True))
                result_writer.writerow(self.tag_with_bigram_tagger(tokens))
                result_writer.writerow(self.tag_with_bigram_tagger(tokens, backoff=True))
                result_writer.writerow(self.tag_with_trigram_tagger(tokens))
                result_writer.writerow(self.tag_with_trigram_tagger(tokens, backoff=True))
                result_writer.writerow(self.tag_with_perceptron_tagger(tokens))
                result_writer.writerow([])

            print("----- POS tagging done\n")


def main():
    current_path = dirname(realpath(__file__))

    csv_file_path = join(current_path, '..', '..', 'data', 'data.csv')
    output_path = join(current_path, "results", "pos_tagging")

    pos_tagger = POSTagger(csv_file_path)
    pos_tagger.tag_random_sentences(5, output_path)

if __name__ == "__main__":
    main()
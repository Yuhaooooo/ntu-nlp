from pathlib import Path

import pandas as pd
import re
import spacy
import random
from os import getcwd
from os.path import join
from nltk.tokenize import sent_tokenize
from collections import Counter

nlp = spacy.load("en_core_web_sm")

numberOfBusinessId = 5
numberOfPairs = 5
withExtra = False


def selectNBusinessId(df, seed=4, business_id_num=5):
    business_id_list = df.business_id.values.tolist()
    random.Random(4).shuffle(business_id_list)

    df_5 = df[df.business_id.isin(business_id_list[:business_id_num])]

    bs_text_map = dict()
    for bid in business_id_list[:business_id_num]:
        bs_text_map[bid] = df_5[df_5['business_id'] == bid].text.tolist()

    print('\n\n{} Selecting {} business ID {}\n'.format('-' * 20, business_id_num, '-' * 20))

    for b in bs_text_map.keys():
        print('Business ID: ', b)

    return bs_text_map


class NounAndAdjPair:
    patterns = ['(ADJ )*(NOUN )+(ADV )*(VERB )+(ADV )*ADJ ',  # The Korean grill is good
                '(NOUN )+.*PRON (VERB )+(ADV )*ADJ ',  # I like the food, which is good
                '(ADV )*ADJ (NOUN )+',  # good service
                ]

    def __init__(self, doc, with_extra=False):

        def get_doc():
            return re.sub(' +', ' ', self.original_doc.replace('\n', ' ').strip()).lower()

        def get_original_sentences():
            return [s for s in sent_tokenize(self.doc)]  # nltk tokenizer

        def get_sentences():
            return [' '.join([w.text for w in nlp(s)]) for s in self.original_sentences]  # spacy word tokenizer

        def get_taggings():
            return [' '.join([w.pos_ for w in nlp(s)]) + ' ' for s in self.original_sentences]

        self.withExtra = with_extra
        self.original_doc = doc
        self.doc = get_doc()
        self.original_sentences = get_original_sentences()
        self.sentences = get_sentences()
        self.taggings = get_taggings()

    #         print(len(self.sentences), len(self.taggings))

    def getPairsWithFSA(self, returnOnlyPairs=False, returnInDf=False):

        def check_if_adj_and_noun_exists(tagging):
            if 'ADJ' in tagging and 'NOUN' in tagging:
                return True
            return False

        def get_wolds_by_tagging_index(target_tagging_index, no_sentence, no_pattern):

            original_sentence = self.sentences[no_sentence]
            original_tagging = self.taggings[no_sentence].strip()

            baseIndex = 0 if target_tagging_index[0] == 0 else len(
                original_tagging[:target_tagging_index[0]].strip().split(' '))
            buildIndex = len(original_tagging[target_tagging_index[0]:target_tagging_index[1]].strip().split(' '))

            trimmed_tagging_list = original_tagging.strip().split(' ')[baseIndex: baseIndex + buildIndex]
            trimmed_sentence_list = original_sentence.split(' ')[baseIndex: baseIndex + buildIndex]

            noun_adj_pair = []

            if no_pattern == 0:  # the first pattern
                if self.withExtra:
                    last_verb_index = len(trimmed_tagging_list) - trimmed_tagging_list[::-1].index('VERB') - 1
                    for i in range(len(trimmed_tagging_list)):
                        if trimmed_tagging_list[i] not in ['ADJ', 'NOUN']:  # filter out adv
                            break
                    noun_adj_pair.append(' '.join(trimmed_sentence_list[:i]))
                    noun_adj_pair.append(' '.join(trimmed_sentence_list[last_verb_index + 1:]))
                else:
                    noun_adj_pair.append(' '.join([trimmed_sentence_list[i] for i in
                                                   [i for i, t in enumerate(trimmed_tagging_list) if t == "NOUN"]]))
                    noun_adj_pair.append(trimmed_sentence_list[-1])


            elif no_pattern == 1:
                if self.withExtra:
                    last_noun_end_index = len(trimmed_tagging_list) - trimmed_tagging_list[::-1].index('NOUN') - 1
                    last_noun_start_index = last_noun_end_index
                    for i in range(last_noun_end_index, 0, -1):
                        if trimmed_tagging_list[i] == 'NOUN':
                            last_noun_start_index = i
                        else:
                            break

                    last_verb_index = len(trimmed_tagging_list) - trimmed_tagging_list[::-1].index('VERB') - 1

                    noun_adj_pair.append(' '.join(trimmed_sentence_list[last_noun_start_index:last_noun_end_index + 1]))
                    noun_adj_pair.append(' '.join(trimmed_sentence_list[last_verb_index + 1:]))
                else:
                    noun_index = [i for i, t in enumerate(trimmed_tagging_list) if t == "NOUN"][::-1]
                    if len(noun_index) == 1:
                        noun_adj_pair.append(' '.join([trimmed_sentence_list[i] for i in noun_index]))
                    else:
                        for noun_start_index in range(1, len(noun_index)):
                            if noun_index[noun_start_index] != noun_index[noun_start_index - 1] - 1:
                                break
                        noun_adj_pair.append(
                            ' '.join([trimmed_sentence_list[i] for i in noun_index[:noun_start_index][::1]]))
                    noun_adj_pair.append(trimmed_sentence_list[-1])


            elif no_pattern == 2:
                if self.withExtra:
                    noun_index = trimmed_tagging_list.index('NOUN')
                    noun_adj_pair.append(' '.join(trimmed_sentence_list[noun_index:]))
                    noun_adj_pair.append(' '.join(trimmed_sentence_list[:noun_index]))
                else:
                    noun_adj_pair.append(' '.join([trimmed_sentence_list[i] for i in
                                                   [i for i, t in enumerate(trimmed_tagging_list) if t == "NOUN"]]))
                    noun_adj_pair.append(trimmed_sentence_list[trimmed_tagging_list.index('ADJ')])

            return tuple(noun_adj_pair)

        def form_df(sentence_adjNoun_pair):
            df = pd.DataFrame(columns=['Sentence', 'AdjNounPair'])
            pd.set_option('display.max_colwidth', -1)
            df.Sentence, df.AdjNounPair = list(sentence_adjNoun_pair.keys()), list(sentence_adjNoun_pair.values())
            return df

        sentence_adjNoun_pair = dict(zip(self.sentences, [[] for i in range(len(self.sentences))]))

        for i in range(len(self.sentences)):
            s = self.sentences[i]
            t = self.taggings[i]

            if check_if_adj_and_noun_exists(t):
                for p in self.patterns:
                    for x in re.finditer(p, t):
                        sentence_adjNoun_pair[s].append(get_wolds_by_tagging_index(x.span(), i, self.patterns.index(p)))

        if returnOnlyPairs:
            pairs = []
            for p in sentence_adjNoun_pair.values():
                pairs.extend(p)
            return pairs

        if returnInDf:
            return form_df(sentence_adjNoun_pair)

        return sentence_adjNoun_pair


def getPairs(bs_text_map, numberOfPairs=5, withExtra=False, returnInDf=True):
    bs_pair_map = dict(zip(list(bs_text_map.keys()), [[] for i in range(len(list(bs_text_map.keys())))]))

    print('\n{} Getting pairs {}\n'.format('-' * 25, '-' * 25))

    for b in list(bs_pair_map.keys()):
        print('Processing reviews from business ID: {} ...'.format(b))
        docs = bs_text_map[b]
        for doc in docs:
            doc_nlp = NounAndAdjPair(doc, with_extra=withExtra)
            bs_pair_map[b].extend(doc_nlp.getPairsWithFSA(returnOnlyPairs=True))

    for bs in list(bs_pair_map.keys()):
        keys = list(Counter(bs_pair_map[bs]).keys())  # equals to list(set(words))
        values = list(Counter(bs_pair_map[bs]).values())
        keys_index = sorted(range(len(values)), key=lambda k: values[k], reverse=True)
        bs_pair_map[bs] = [(keys[i], values[i]) for i in keys_index[:numberOfPairs]]

    if returnInDf:
        df = pd.DataFrame(columns=['BusinessId', 'AdjNounPair'])
        df.BusinessId, df.AdjNounPair = list(bs_pair_map.keys()), list(bs_pair_map.values())
        df.to_csv(join(getcwd(), 'core', 'examples', '3.3-Adj-Noun-Pairs', 'adj_noun_pairs1.csv'))
        return df

    return bs_pair_map


if __name__ == "__main__":
    df = pd.read_csv(Path(__file__).absolute().parent / '../../data/data.csv')

    businessPairs = getPairs(selectNBusinessId(df, business_id_num=numberOfBusinessId), numberOfPairs=numberOfPairs,
                             withExtra=withExtra)

    print('\n\n\n{} RESULT {}\n\n'.format('-' * 28, '-' * 28))

    print(businessPairs.values)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# conda install spacy
# pip install bert_score
import collections
import json
import spacy
import os
import pandas as pd
from bert_score import score
import torch
from string import punctuation
import pickle

nlp = spacy.load("en_core_web_sm")

def pos_tagging(text):
    adj_list = []
    noun_list = []

    doc = nlp(text)

    for token in doc:
        if token.pos_ == 'ADJ':
            adj_list.append(token.text)
        elif token.pos_ == 'NOUN':
            noun_list.append(token.text)

    return adj_list, noun_list

def pre_processing(text):
    doc = nlp(text)

    text = [token for token in doc if not token.is_stop and token.is_alpha]

    text = [token.text for token in text]

    return ' '.join(text)

def read_a_business(review_list):

    most_useful_adj_list = []
    most_useful_noun_list = []

    most_useful_adj_counter = collections.Counter()
    most_useful_noun_counter = collections.Counter()

    pair_list = []
    for text in review_list:
        adj_list, noun_list = pos_tagging(text)

        if adj_list == [] or noun_list == []:
            continue

        text = pre_processing(text)

        P_noun, _, _ = score(noun_list, len(noun_list)*[text], "bert-base-uncased")
        P_adj, _, _  = score(adj_list, len(adj_list)*[text], "bert-base-uncased")

        adj_index = torch.argmax(P_adj).item()
        noun_index = torch.argmax(P_noun).item()


        pair = tuple((adj_list[adj_index], noun_list[noun_index]))
        pair_list.append(pair)

    return pair_list

def read_all_businesses(business_id_list):

    adj_lists = {}
    noun_lists = {}

    df = pd.read_csv("data.csv")
    df = df.to_dict(orient='records')

    print(len(df))

    business_id_list_dict = dict(zip(business_id_list, [[],[],[],[],[],[]]))


    print(business_id_list_dict)

    for json_element in df:
        if json_element['business_id'] in business_id_list and len(business_id_list_dict[json_element['business_id']]) < 100: 
            business_id_list_dict[json_element['business_id']].append(json_element['text'])


    for business_id in business_id_list:
        review_list = business_id_list_dict[business_id]

        print(len(review_list))
        pair_counter = collections.Counter()
        pair_counter.update(read_a_business(review_list))


        print(pair_counter)

read_all_businesses(['8Z72HW5ydzQFydUxZglurg',
                    'QeEQXdto_4wFRaNKyIygRA',
                    'IUMyUYOIR9UQ7XGIEQKOuA',
                    'Rii85bzYKGC9P0zOyAem6A',
                    'i-2OzvZUDtvKCMq1vcRSZg'])

import pickle

import torch

from torchtext.data import Field, LabelField, TabularDataset, BucketIterator
from string import punctuation


def text_field_preprocessing(tokens: list):
    return list(filter(lambda token: token not in punctuation, tokens))


TEXT = Field(preprocessing=text_field_preprocessing, sequential=True, tokenize='spacy', lower=True)
LABEL = LabelField(dtype=torch.float)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def get_iterator():
    DATA_DIR = '../data'

    tv_datafields = [('stars', LABEL), ('text', TEXT)]

    trn, vld = TabularDataset.splits(
        path=DATA_DIR,  # the root directory where the data lies
        train='train1.csv', validation="val1.csv",
        format='csv',
        skip_header=True,
        fields=tv_datafields)

    MAX_VOCAB_SIZE = 100
    TEXT.build_vocab(trn, max_size=MAX_VOCAB_SIZE)
    LABEL.build_vocab(trn)

    with open('text_fields.pkl', 'wb') as f:
        pickle.dump(TEXT, f)

    BATCH_SIZE = 64

    train_iterator, valid_iterator = BucketIterator.splits(
        (trn, vld),
        batch_size=BATCH_SIZE,
        sort_key=lambda x: len(x.text),
        device=device)

    return train_iterator, valid_iterator

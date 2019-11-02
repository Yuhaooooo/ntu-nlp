import pickle
from pathlib import Path

import torch

from torchtext.data import Field, LabelField, TabularDataset, BucketIterator
from string import punctuation


def text_field_preprocessing(tokens: list):
    return list(filter(lambda token: token not in punctuation, tokens))


TEXT = Field(preprocessing=text_field_preprocessing, sequential=True, tokenize='spacy', lower=True)
LABEL = LabelField(dtype=torch.float)
MAX_VOCAB_SIZE = 30000
BATCH_SIZE = 128
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
DATA_DIR = Path(__file__).absolute().parent / '../data'


def save_text_fields():
    with open('text_fields.pkl', 'wb') as f:
        pickle.dump(TEXT, f)


def get_iterator():
    tv_datafields = [('stars', LABEL), ('text', TEXT)]

    trn, vld = TabularDataset.splits(
        path=DATA_DIR,  # the root directory where the data lies
        train='train.csv', validation="val.csv",
        format='csv',
        skip_header=True,
        fields=tv_datafields)

    TEXT.build_vocab(trn, vectors="glove.6B.300d")
    LABEL.build_vocab(trn)

    train_iterator, valid_iterator = BucketIterator.splits(
        (trn, vld),
        batch_size=BATCH_SIZE,
        sort_key=lambda x: len(x.text),
        device=device)

    return train_iterator, valid_iterator

import os
import pickle
import os.path as osp

import torch

from torchtext.data import Field, LabelField, TabularDataset, BucketIterator
from string import punctuation

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def text_field_preprocessing(tokens: list):
    return list(filter(lambda token: token not in punctuation, tokens))


def build_field():
    TEXT = Field(preprocessing=text_field_preprocessing, sequential=True, tokenize='spacy', lower=True)
    LABEL = LabelField(dtype=torch.float)
    datafields = [('stars', LABEL), ('text', TEXT)]
    return datafields


def save_text_fields(field, output_dir: str):
    save_name = osp.join(output_dir, 'fields.pkl')
    with open(save_name, 'wb') as f:
        pickle.dump(field, f)


def get_iterator(datafields, data_dir, bs):
    trn, vld = TabularDataset.splits(
        path=data_dir,
        train='train.csv', validation="val.csv",
        format='csv',
        skip_header=True,
        fields=datafields)
    _, label_field = datafields[0]
    _, text_field = datafields[1]

    text_field.build_vocab(trn, vectors="glove.6B.100d")
    label_field.build_vocab(trn)

    train_iterator, valid_iterator = BucketIterator.splits(
        (trn, vld),
        batch_size=bs,
        sort_key=lambda x: len(x.text),
        device=device)

    return train_iterator, valid_iterator

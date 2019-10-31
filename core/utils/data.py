import torch

from torchtext.data import Field, LabelField, TabularDataset, BucketIterator
from string import punctuation


def text_field_preprocessing(tokens: list):
    return list(filter(lambda token: token not in punctuation, tokens))


TEXT = Field(preprocessing=text_field_preprocessing, sequential=True, tokenize='spacy', lower=True)
LABEL = LabelField(dtype=torch.float)

DATA_DIR = '../data'

tv_datafields = [('stars', LABEL), ('text', TEXT)]

trn, vld = TabularDataset.splits(
    path=DATA_DIR,  # the root directory where the data lies
    train='train.csv', validation="val.csv",
    format='csv',
    skip_header=True,
    fields=tv_datafields)

MAX_VOCAB_SIZE = 10000
TEXT.build_vocab(trn, max_size=MAX_VOCAB_SIZE)
LABEL.build_vocab(trn)

print(TEXT.vocab.freqs.most_common(10))
print(len(LABEL.vocab))

BATCH_SIZE = 64

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

train_iterator, valid_iterator = BucketIterator.splits(
    (trn, vld),
    batch_size=BATCH_SIZE,
    device=device)

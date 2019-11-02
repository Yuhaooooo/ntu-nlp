import pickle

import os.path as osp
# noinspection PyUnresolvedReferences
import spacy
import torch
import torch.nn as nn
from torchtext.data import BucketIterator

from core.configs import OUTPUT_DIR
from core.models.sentiment import RNN
from core.utils.TabularDatasetFromList import TabularDatasetFromList

# noinspection PyUnresolvedReferences
from core.utils.data import text_field_preprocessing

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open(osp.join(OUTPUT_DIR, 'fields.pkl'), 'rb') as vocab_f:
    text_field = pickle.load(vocab_f)

predict_datafield = [('text', text_field)]


test_dataset = TabularDatasetFromList(
    input_list=[['This is an example'], ['The food is very delicious, I love this restaurant']],
    format='csv',
    fields=predict_datafield)

test_iterator = BucketIterator(
    test_dataset,
    batch_size=1,
    sort_key=lambda x: len(x.text),
    device=device,
    train=False)

model: nn.Module = RNN(text_field)
model.cuda()
model.load_state_dict(torch.load(osp.join(OUTPUT_DIR, 'sentiment-model.pt')))
model.eval()

output = None
for batch in test_iterator:
    output = model(batch.text)
    print(output)

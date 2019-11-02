import pickle

import os.path as osp
# noinspection PyUnresolvedReferences
import spacy
import torch
import torch.nn as nn
from torchtext.data import BucketIterator

from configs import OUTPUT_DIR
from models.sentiment import RNN
from utils.TabularDatasetFromList import TabularDatasetFromList

# noinspection PyUnresolvedReferences
from utils.data import text_field_preprocessing

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open(osp.join(OUTPUT_DIR, 'fields.pkl'), 'rb') as vocab_f:
    text_field = pickle.load(vocab_f)

predict_datafield = [('text', text_field)]

test_dataset = TabularDatasetFromList(
    input_list=[[
        "Come here at least 2x a month. Get the same thing. NY strip steak with sweet potato and veggies! Always comes hot and cook to perfect order. It's always chaos in there but the servers never mess up and never long wait on food. Appreciate the call ahead seating! Always a joy to go in n sit down with in 15 mins MAX! Thanks for awesome food and service!"
    ], ["delicious, grubby, chinese food in generous portions and always great service. their szchewaun chicken is THE BOMB. so spicy it makes me sweat."]],
    format='csv',
    fields=predict_datafield)

test_iterator = BucketIterator(
    test_dataset,
    batch_size=1,
    sort_key=lambda x: len(x.text),
    device=device,
    train=False)

model: nn.Module = RNN(text_field)
model.to(device)
model.load_state_dict(torch.load(osp.join(OUTPUT_DIR, 'sentiment-model.pt')))
model.eval()

output = None
for batch in test_iterator:
    output = model(batch.text).reshape(-1).tolist()
    print(output)

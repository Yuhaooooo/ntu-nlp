import pickle

import spacy
import torch
from torchtext.data import BucketIterator

from core.models.emotional import RNN
from core.utils.TabularDatasetFromList import TabularDatasetFromList

# noinspection PyUnresolvedReferences
from core.utils.data import text_field_preprocessing

with open('../utils/text_fields.pkl', 'rb') as vocab_f:
    text_field = pickle.load(vocab_f)

predict_datafield = [('text', text_field)]

text = 'Some text is input into a neural network'


def words2id(words_tokenized, vocab):
    vocab_dict = dict(vocab)
    id_list = []
    for i in words_tokenized:
        try:
            id_list.append(float(vocab_dict[i]))
        except KeyError:
            id_list.append(float(10000))

    return id_list


# nlp = spacy.load('en')
# doc = nlp(text)
# tokenized = [token.text for token in doc]
# batch_one_data = torch.ones((1, 100), dtype=torch.long).cuda()


test_dataset = TabularDatasetFromList(
    input_list=[['This is an example'], ['The food is very delicious, I love this restaurant']],
    format='csv',
    fields=predict_datafield)

test_iterator = BucketIterator(
    test_dataset,
    batch_size=1,
    sort_key=lambda x: len(x.text),
    device='cuda',
    train=False)

model = RNN(102, 128, 256, 1)
model.cuda()
model.load_state_dict(torch.load('tut1-model.pt'))
model.eval()

output = None
for batch in test_iterator:
    output = model(batch.text)
    print(output)

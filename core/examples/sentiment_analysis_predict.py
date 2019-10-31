import torch

from core.models.emotional import RNN

text = 'Some text'

model = RNN(100, 128, 256, 1)
model.load_state_dict(torch.load('tut1-model.pt'))

### preprocess
output = model(text)
print(output)

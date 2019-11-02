import torch
import torch.nn as nn
from torchtext.data import Field
from core.configs import configs


class RNN(nn.Module):
    def __init__(self, text_field: Field):
        super().__init__()
        model_config = configs['model']
        # noinspection PyArgumentList
        self.embedding = nn.Embedding.from_pretrained(torch.FloatTensor(text_field.vocab.vectors), freeze=True,
                                                      max_norm=2)
        self.rnn = nn.GRU(model_config['embedding'], model_config['hidden'], num_layers=1)
        self.fc = nn.Linear(model_config['hidden'], model_config['output'])
        self.nnDropout = nn.Dropout(model_config['dropout'])

    def forward(self, text: torch.Tensor):
        embedded = self.embedding(text)
        output, hidden = self.rnn(self.nnDropout(embedded))
        assert torch.equal(output[-1, :, :], hidden.squeeze(0))
        return self.fc(hidden.squeeze(0))

    def predict(self, text: str):
        pass

    def batch_predict(self, texts: list):
        pass

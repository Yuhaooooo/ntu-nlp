import torch
import torch.nn as nn
from torchtext.data import Field


class RNN(nn.Module):
    def __init__(self, embedding_dim, hidden_dim, output_dim, text_field: Field):
        super().__init__()
        # noinspection PyArgumentList
        self.embedding = nn.Embedding.from_pretrained(torch.FloatTensor(text_field.vocab.vectors), freeze=True,
                                                      max_norm=2)
        self.rnn = nn.GRU(embedding_dim, hidden_dim, num_layers=1)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.nnDropout = nn.Dropout(0.2)

    def forward(self, text):
        embedded = self.embedding(text)
        output, hidden = self.rnn(self.nnDropout(embedded))
        assert torch.equal(output[-1, :, :], hidden.squeeze(0))
        return self.fc(hidden.squeeze(0))

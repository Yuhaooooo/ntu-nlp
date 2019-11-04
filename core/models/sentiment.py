import torch
import torch.nn as nn
from torchtext.data import Field
from configs import configs


def init_lstm_wt(lstm):
    for names in lstm._all_weights:
        for name in names:
            if name.startswith('weight_'):
                wt = getattr(lstm, name)
                wt.data.uniform_(configs['rand_unif_init_mag'], configs['rand_unif_init_mag'])
            elif name.startswith('bias_'):
                # set forget bias to 1
                bias = getattr(lstm, name)
                n = bias.size(0)
                start, end = n // 4, n // 2
                bias.data.fill_(0.)
                bias.data[start:end].fill_(1.)


def init_linear_wt(linear):
    linear.weight.data.normal_(std=float(configs['trunc_norm_init_std']))
    if linear.bias is not None:
        linear.bias.data.normal_(std=float(configs['trunc_norm_init_std']))


class RNN(nn.Module):
    def __init__(self, text_field: Field):
        super().__init__()
        model_config = configs['model']
        # noinspection PyArgumentList
        self.embedding = nn.Embedding.from_pretrained(torch.FloatTensor(text_field.vocab.vectors), freeze=True,
                                                      max_norm=2)
        self.rnn = nn.GRU(model_config['embedding'], model_config['hidden'], num_layers=1)
        init_lstm_wt(self.rnn)

        self.fc = nn.Linear(model_config['hidden'], model_config['output'])
        init_linear_wt(self.fc)
        self.nnDropout = nn.Dropout(model_config['dropout'])

    def forward(self, text: torch.Tensor):
        embedded = self.embedding(text)
        output, hidden = self.rnn(self.nnDropout(embedded))
        assert torch.equal(output[-1, :, :], hidden.squeeze(0))
        return self.fc(hidden.squeeze(0))

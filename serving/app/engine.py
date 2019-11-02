import pickle
# noinspection PyUnresolvedReferences
import spacy
import torch
from torch import nn
from torchtext.data import BucketIterator

from models.sentiment import RNN
from utils.TabularDatasetFromList import TabularDatasetFromList
# noinspection PyUnresolvedReferences
from utils.data import text_field_preprocessing


class SentimentService(object):
    def __init__(self, model_file_path, text_field_path, device):
        self.device = device
        with open(text_field_path, 'rb') as f:
            text_field = pickle.load(f)
            self.model: nn.Module = RNN(text_field)
        self.model.to(device)
        self.model.load_state_dict(torch.load(model_file_path, map_location=device))
        self.model.eval()

        self.predict_field = [('text', text_field)]

    def single_predict(self, text: str):
        iterator = self.preprocessing([text])
        output = None
        for batch in iterator:
            output = self.model(batch.text).item()
        return output

    def batch_predict(self, batch_text, batch_size):
        iterator = self.preprocessing(batch_text, batch_size)
        output = []
        for batch in iterator:
            output.extend(self.model(batch.text).reshape(-1).tolist())
        return output

    def preprocessing(self, batch_text: list, batch_size: int = 1):
        batch_text_list = map(lambda x: [x], batch_text)
        test_dataset = TabularDatasetFromList(
            input_list=batch_text_list,
            format='csv',
            fields=self.predict_field)
        test_iterator = BucketIterator(
            test_dataset,
            batch_size=batch_size,
            sort_key=lambda x: len(x.text),
            device=self.device,
            train=False)
        return test_iterator

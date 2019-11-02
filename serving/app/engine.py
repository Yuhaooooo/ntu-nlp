# noinspection PyUnresolvedReferences
import spacy
from torch import nn
from torchtext.data import BucketIterator

from models.sentiment import RNN
from utils.TabularDatasetFromList import TabularDatasetFromList
# noinspection PyUnresolvedReferences
from utils.data import text_field_preprocessing


class ReviewService(object):
    def __init__(self, model_file, text_field, device):
        self.device = device

        self.model: nn.Module = RNN(text_field)
        self.model.to(device)
        self.model.load_state_dict(model_file)
        self.model.eval()

        self.predict_field = [('text', text_field)]

    def single_predict(self, text: str):
        iterator = self.preprocessing([text])
        output = None
        for batch in iterator:
            output = self.model(batch.text).item()
        result = {'output': output[0]}

        return result

    def batch_predict(self, batch_text, batch_size):
        iterator = self.preprocessing(batch_text, batch_size)
        output = []
        for batch in iterator:
            output.extend(self.model(batch.text).item())
        result = {'output': output}

        return result

    def preprocessing(self, batch_text: list, batch_size: int = 1):
        test_dataset = TabularDatasetFromList(
            input_list=[batch_text],
            format='csv',
            fields=self.predict_field)
        test_iterator = BucketIterator(
            test_dataset,
            batch_size=batch_size,
            sort_key=lambda x: len(x.text),
            device=self.device,
            train=False)
        return test_iterator

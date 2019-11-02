import torch
import torch.nn as nn

from configs import DATA_DIR, OUTPUT_DIR
from models.sentiment import RNN
from utils.data import get_iterator, build_field, save_text_fields
import torch.optim as optim

import os.path as osp

from tqdm import trange

BATCH_SIZE = 128
LR = 1e-4
N_EPOCHS = 200
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def binary_accuracy(preds, y):
    """
    Returns accuracy per batch, i.e. if you get 8/10 right, this returns 0.8, NOT 8
    """

    # round predictions to the closest integer
    rounded_preds = torch.round(preds)
    correct = (rounded_preds == y).float()  # convert into float for division
    acc = correct.sum() / len(correct)
    return acc


def train(model, iterator, optimizer, criterion):
    epoch_loss = 0
    epoch_acc = 0

    model.train()

    for batch in iterator:
        optimizer.zero_grad()
        predictions = model(batch.text).squeeze(1)
        loss = criterion(predictions, batch.stars)
        acc = binary_accuracy(predictions, batch.stars)
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()
        epoch_acc += acc.item()

    return epoch_loss / len(iterator), epoch_acc / len(iterator)


def evaluate(model, iterator, criterion):
    epoch_loss = 0
    epoch_acc = 0

    model.eval()

    with torch.no_grad():
        for batch in iterator:
            predictions = model(batch.text).squeeze(1)
            loss = criterion(predictions, batch.stars)
            acc = binary_accuracy(predictions, batch.stars)

            epoch_loss += loss.item()
            epoch_acc += acc.item()

    return epoch_loss / len(iterator), epoch_acc / len(iterator)


if __name__ == '__main__':
    data_field = build_field()
    train_iterator, valid_iterator = get_iterator(data_field, bs=BATCH_SIZE, data_dir=DATA_DIR)
    _, text_field = data_field[1]
    save_text_fields(text_field, OUTPUT_DIR)

    model: nn.Module = RNN(text_field)
    optimizer = optim.Adam(model.parameters(), lr=LR)
    criterion = nn.MSELoss()
    model = model.to(device)
    criterion = criterion.to(device)

    best_valid_loss = float('inf')
    t = trange(N_EPOCHS, desc='')
    for epoch in t:
        train_loss, train_acc = train(model, train_iterator, optimizer, criterion)
        valid_loss, valid_acc = evaluate(model, valid_iterator, criterion)

        if valid_loss < best_valid_loss:
            best_valid_loss = valid_loss
            torch.save(model.state_dict(), osp.join(OUTPUT_DIR, 'sentiment-model.pt'))

        t.set_description('Train Loss: {:.3f} | Train Acc: {:.2f}% | Val. Loss: {:.3f} |  Val. Acc: {:.2f}%'
                          .format(train_loss, train_acc * 100, valid_loss, valid_acc * 100))

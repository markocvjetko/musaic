from torch.utils.data import DataLoader
from File_util import *
import torch.nn as nn
from helper import *
from constants import *
from model import SkipGram_Model
from word2vec.dataset import SkipGramW2vDataset

if __name__ == '__main__':

    raw_data = read_files(list_files_recursive('../data', extension='988-aria.cary'))
    dataset = SkipGramW2vDataset(raw_data, SKIPGRAM_WINDOW_SIZE)

    train_size = int(SKIPGRAM_TRAIN_SIZE * len(dataset))
    val_size = len(dataset) - train_size

    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

    train_dataloader = DataLoader(train_dataset, SKIPGRAM_DL_BATCH_SIZE, shuffle=True)
    val_dataloader = DataLoader(val_dataset, SKIPGRAM_DL_BATCH_SIZE, shuffle=False)

    model = SkipGram_Model(vocab_size=len(dataset.vocab))
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.025)

    for epoch in range(1):  # loop over the dataset multiple times

        running_loss = 0.0
        for i, data in enumerate(train_dataloader, 0):
            # get the inputs
            inputs, labels = data['inputs'], data['labels']

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 2000 == 1999:  # print every 2000 mini-batches
                print('[%d, %5d] loss: %.3f' %
                      (epoch + 1, i + 1, running_loss / 2000))
                running_loss = 0.0
    save_model(model.state_dict(), 'skip-gram.pt')
    print('Finished Training')

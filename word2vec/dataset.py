import torch
from torch import nn
from torch.utils.data import Dataset
from analysis_util import vocabulary, word_index_map
from ngram import tokenize
from text_preprocessing import Tokenizers
import torch.nn.functional as F


class SkipGramW2vDataset(Dataset):
    def __init__(self, corpus, window_size):
        assert window_size > 0, f"window_size greater than 0 expected, got: {window_size}"
        self.window_size = window_size

        tokenized_corpus = [tokenize(text, Tokenizers.CHARACTER) for text in corpus]

        self.vocab = vocabulary(tokenized_corpus)
        self.word_indices = word_index_map(self.vocab)

        self.indiced_corpus = []
        for tokenized_text in tokenized_corpus:
            self.indiced_corpus.append([self.word_indices[token] for token in tokenized_text])




    def __len__(self):
        length = 0
        for t in self.indiced_corpus:
            length += max(0, len(t) - 2 * self.window_size)
        return length


    def __getitem__(self, index):
        curr_len = 0
        for t in self.indiced_corpus:
            if curr_len + max(0, len(t) - 2*self.window_size) <= index:
                curr_len += max(0, len(t) - 2*self.window_size)
            else:
                inputs = t[index - curr_len + self.window_size]

                inputs_tensor = torch.tensor(inputs)

                labels = list(t[index - curr_len: index - curr_len + self.window_size])
                labels.extend(t[index - curr_len + self.window_size + 1: index - curr_len + 2 * self.window_size + 1])

                labels_tensor = nn.functional.one_hot(torch.tensor(labels), num_classes=len(self.vocab))
                labels_tensor = torch.max(labels_tensor, axis=0).values
                labels_tensor = labels_tensor.type(torch.FloatTensor)
                break

        return {'inputs' : inputs_tensor, 'labels' : labels_tensor}

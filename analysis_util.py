import glob
import os

from nltk.translate.bleu_score import SmoothingFunction, corpus_bleu, sentence_bleu

from File_util import read_files, list_files_recursive
from ngram import tokenize


def vocab(corpus):
    '''
    Returns the vocabulary across a list of textual data
    :param dataset:
    :return: list of words, vocabulary
    '''
    vocab = set()
    [vocab.add(word) for text in corpus for word in tokenize(text)]
    return list(vocab)

def corpus_length(corpus):
    len_sum = sum([len(tokenize(sentence)) for sentence in corpus])
    return len_sum

if __name__ == "__main__":
    data = read_files(list_files_recursive('data', 'cary'))
    v = vocab(data)
    print(len(v))
    print(corpus_length(data))
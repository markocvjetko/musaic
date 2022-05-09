import glob
import os

from nltk.translate.bleu_score import SmoothingFunction, corpus_bleu, sentence_bleu

from File_util import read_files, list_files_recursive
from ngram import tokenize


def vocabulary(corpus):
    '''
    Returns the vocabulary across a list of textual data
    :param dataset:
    :return: list of words, vocabulary
    '''
    vocab = set()
    [vocab.add(token) for piece in corpus for token in piece]
    return list(vocab)

def corpus_length(corpus):
    len_sum = sum([len(tokenize(sentence)) for sentence in corpus])
    return len_sum

def word_index_map(vocabulary):
    word_index_dict = {}
    for i, word in enumerate(vocabulary):
        word_index_dict[word] = i
    return word_index_dict

if __name__ == "__main__":
    data = read_files(list_files_recursive('data', 'cary'))
    v = vocabulary(data)
    print(len(v))
    print(corpus_length(data))
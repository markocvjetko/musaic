import glob
import os
import random


class Ngram():

    def __init__(self, n):
        self.n = n
        self.contexts = {}
        self.ngram_counter = {}
        self.tokens = set()
    def update(self, text):
        tokens = tokenize(text)
        self.tokens.update(tokens)
        new_ngrams = get_ngrams(tokens, self.n)

        for new_ngram in new_ngrams:
            if new_ngram in self.ngram_counter.keys():
                self.ngram_counter[new_ngram] += 1
            else:
                self.ngram_counter[new_ngram] = 1

            context = new_ngram[:-1]
            word = new_ngram[-1]

            if context in self.contexts:
                self.contexts[context].add(word)
            else:
                self.contexts[context] = {word}

    def get_probability(self, token, context):

        ngram_count = self.ngram_counter[context + (token,)]
        possible_tokens = self.contexts[context]

        try:
            context_count = 0
            for possible_token in possible_tokens:
                context_count += self.ngram_counter[context + (possible_token,)]
        except:
            return 0
        return ngram_count / context_count

    def generate_random_token(self, context):
        token_probabilities = {}
        rand_num = random.random() * 1.05
        for possible_token in self.contexts[context]:
            probability = self.get_probability(possible_token, context)
            token_probabilities[possible_token] = probability

        if rand_num > 1.0:
            return random.sample(self.tokens, 1)[0]
        probability_sum = 0
        for token in sorted(token_probabilities):
            probability_sum += token_probabilities[token]
            if probability_sum > rand_num:
                return token

def tokenize(text):
    '''
    Removes leading and trailing whitespaces, then splits the string after every
    whitespace. Multiple whitespaces result in empty tokens.
    :param text: Text string to be tokenized.
    :return: List of tokens.
    '''
    return text.strip().split(' ')

def detokenize(tokens, delim=' '):
    '''
    Merges tokens into a single string.
    :param tokens: List of tokens.
    :return: String of concatenated tokens.
    '''
    return ' '.join(tokens)

def get_ngrams(tokens, n):
    '''
    
    Creates ngrams (token tuples) from a given list of tokens.
    :param tokens: List of tokens 
    :return: List of ngrams (token tuples)
    '''
    ngrams = []
    for i in range(len(tokens) - n + 1):
        ngrams.append(tuple(tokens[i:i+n]))
    return ngrams

def read_file(path):
    text_file = open(path, "r")
    data = text_file.read()
    text_file.close()
    return data

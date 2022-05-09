from enum import Enum

class Tokenizers(Enum):
    WHITESPACE = 1
    CHARACTER = 2


def tokenize(text, type=Tokenizers.WHITESPACE):
    '''
     Removes leading and trailing whitespaces, then tokenizes the text.
    :param text: Text string to be tokenized
    :param type:
    :return: List of tokens
    '''

    text = text.strip()
    if type == Tokenizers.WHITESPACE:
        return whitespace_tokenize(text)
    if type == Tokenizers.CHARACTER:
        return character_tokenize(text)


def whitespace_tokenize(text):
    '''
    Splits the text after every
    whitespace. Multiple whitespaces result in empty tokens.
    :param text: Text string to be tokenized.
    :return: List of tokens.
    '''
    return text.strip().split(' ')


def character_tokenize(text):
    '''
    Creates a token from every character in the text,
    :param text: Text string to be tokenized
    :return: List of tokens
    '''
    return list(text.strip())


def detokenize(tokens, delim=' '):
    '''
    Merges tokens into a single string.
    :param tokens: List of tokens.
    :return: String of concatenated tokens.
    '''
    return delim.join(tokens)


def get_ngrams(tokens, n):
    '''

    Creates ngrams (token tuples) from a given list of tokens.
    :param tokens: List of tokens
    :return: List of ngrams (token tuples)
    '''
    ngrams = []
    for i in range(len(tokens) - n + 1):
        ngrams.append(tuple(tokens[i:i + n]))
    return ngrams

from nltk.lm.preprocessing import padded_everygram_pipeline

from ngram import detokenize
from parse_util import carycompressed_to_midicsv
from text_nltk_texgen import *
from File_util import *
from nltk.lm import MLE

from text_preprocessing import tokenize


def generate_text(model, num_words, random_seed=42):
    """
    :param model: An ngram language model from `nltk.lm.model`.
    :param num_words: Max no. of words to generate.
    :param random_seed: Seed value for random.
    """
    content = []
    for token in model.generate(num_words, random_seed=random_seed):
        if token == '<s>':
            continue
        if token == '</s>':
            break
        content.append(token)
    return detokenize(content)

if __name__ == "__main__":

    n = 2
    gen_length = 500
    seed = 70

    music = read_files(list_files_recursive('data', '.cary'))
    tokens = [tokenize(piece) for piece in music]
    train, vocab = padded_everygram_pipeline(n, tokens)
    model = MLE(n)
    model.fit(train, vocab)
    music = generate_text(model, gen_length, seed)
print(music)
print(carycompressed_to_midicsv(music))
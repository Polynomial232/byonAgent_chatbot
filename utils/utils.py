import re
import numpy as np
from more_itertools import locate

def word_extraction(sentence):
    words = re.sub("[^\w]", " ",  sentence.lower()).split()
    return words

def tokenize(sentences):
    words = []
    for sentence in sentences:
        w = word_extraction(sentence)
        words.extend(w)            
        words = sorted(list(set(words)))   
    return words

def get_bag_of_word(sentence, allsentences):
    words = word_extraction(sentence)
    vocab = tokenize(allsentences)
    bag_vector = np.zeros(len(vocab))
    for w in words:
        for i,word in enumerate(vocab):
            if word == w:                     
                bag_vector[i] = 1

    return np.array(bag_vector)

def compare_bag_of_word(sentence_bag, all_bag):
    indices = locate(sentence_bag, lambda x: x == 1)
    indices = list(indices)

    percent = []
    for bag_of_word in all_bag:
        get_bags = bag_of_word[indices]
        percent.append(list(get_bags).count(1) / len(indices))

    max_indices = locate(percent, lambda x: x == max(percent))
    max_indices = list(max_indices)
    get_index = max_indices[0]

    if len(max_indices) > 1:
        return -1

    if percent[0] < 0.8:
        return -1

    return get_index
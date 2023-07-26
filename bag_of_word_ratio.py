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
                bag_vector[i] += 1

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

    print(max_indices)
    if len(max_indices) > 1:
        print("Ditemukan lebih dari 1 data")
    else:
        print("data berada di index: ", get_index)

allsentences = ["BCD ayam bakar", "ABC ayam bakar", "BDC ayam geprek"]
input_user = "saya mau pesan ayam abc"

all_bag_of_words = []
for sentence in allsentences:
    all_bag_of_words.append(get_bag_of_word(sentence, allsentences))

all_bag_of_words = np.array(all_bag_of_words)
sentence_bag_of_word = get_bag_of_word(input_user, allsentences)

compare_bag_of_word(sentence_bag_of_word, all_bag_of_words)
import numpy as np

def load_en():
    embeddings_dict = dict()
    f = open('./data/cc.en.300.vec')
    lines = f.readlines()

    for line in lines[1:]:
        values = line.split()
        word = values[0]
        vec = np.asarray(values[1:], dtype='float32')
        embeddings_dict[word] = vec

    f.close()

    return embeddings_dict

def load_de():
    embeddings_dict = dict()
    f = open('./data/cc.de.300.vec')
    lines = f.readlines()

    for line in lines[1:]:
        values = line.split()
        word = values[0]
        vec = np.asarray(values[1:], dtype='float32')
        embeddings_dict[word] = vec

    f.close()

    return embeddings_dict
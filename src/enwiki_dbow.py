#python example to train doc2vec model (with or without pre-trained word embeddings)

import gensim.models as g
import logging
import common_utils

config = common_utils.get_config()

#pretrained word embeddings
pretrained_emb = "toy_data/pretrained_word_embeddings.txt" #None if use without pretrained embeddings

#enable logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#train doc2vec model
model = g.Doc2Vec.load(config.enwiki_dbow)
print(model)

# import modules & logging
import gensim, logging

# set up logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# input file
sentences = [ ['Athens'], ['Korea'] ]

# train word2vec on the two sentences
model = gensim.models.Word2Vec(sentences, size = 200, min_count = 1, workers = 2, )

fname = "trained_model.txt"
# store the trained model
model.save(fname)

model1 = gensim.models.Word2Vec.load(fname)  # you can continue training with the loaded model!
#model1.train(sentences)
print model1.similarity('Athens', 'Korea')

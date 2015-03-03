# import modules & logging
import gensim, logging

# set up logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# input file
sentences = []

sentences = gensim.models.word2vec.LineSentence('PaperAuthor.csv')

# convert to "multiword" sentences
bigram_transformer = gensim.models.Phrases(sentences)

# train word2vec on the two sentences
model = gensim.models.Word2Vec(bigram_transformer[sentences], size = 200, min_count = 1, workers = 4)

fname = "trained_model.txt"
# store the trained model
model.save(fname)

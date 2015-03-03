# import modules & logging
import gensim, logging

# set up logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# input file
# sentences = [ ["athens"], ["test"], ["test", "data"], ["data"]]

sentences = gensim.models.word2vec.LineSentence('PaperAuthor.csv')

# train word2vec
model = gensim.models.Word2Vec(sentences, window = 1, size = 100, min_count = 5, workers = 4, iter = 5)

fname = "trained_model.txt"

# store the trained model
model.save(fname)

# save the model for each 5 epochs

for i in range(1,20):
    # load stored model
    model = gensim.models.Word2Vec.load(fname)

    # train word2vec
    model = gensim.models.Word2Vec(sentences, window = 1, size = 100, min_count = 5, workers = 4, iter = 5)

    # filename to save model
    fname = "trained_model" + "_" + str(i*5+5) + ".txt"

    # store the trained model
    model.save(fname)

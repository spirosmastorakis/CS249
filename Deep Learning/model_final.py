# import modules & logging
import gensim, logging

# set up logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# input file
# sentences = [ ["athens"], ["test"], ["test", "data"], ["data"]]

# sentences = gensim.models.word2vec.LineSentence('PaperAuthor.csv')
sentences = gensim.models.word2vec.LineSentence('input(3combined).csv')

# train word2vec
model = gensim.models.word2vec.Word2Vec(sentences, window = 2, size = 12, min_count = 5, workers = 4, iter = 50)

fname = "trained_model_50.txt"

# store the trained model
model.save(fname)

model1 = gensim.models.word2vec.Word2Vec(sentences, window = 2, size = 12, min_count = 5, workers = 4, iter = 55)

fname = "trained_model_55.txt"

# store the trained model
model1.save(fname)

model2 = gensim.models.word2vec.Word2Vec(sentences, window = 2, size = 12, min_count = 5, workers = 4, iter = 60)

fname = "trained_model_60.txt"

# store the trained model
model2.save(fname)

model3 = gensim.models.word2vec.Word2Vec(sentences, window = 2, size = 12, min_count = 5, workers = 4, iter = 65)

fname = "trained_model_65.txt"

# store the trained model
model3.save(fname)

model4 = gensim.models.word2vec.Word2Vec(sentences, window = 2, size = 12, min_count = 5, workers = 4, iter = 70)

fname = "trained_model_70.txt"

# store the trained model
model4.save(fname)

model5 = gensim.models.word2vec.Word2Vec(sentences, window = 2, size = 12, min_count = 5, workers = 4, iter = 75)

fname = "trained_model_75.txt"

# store the trained model
model5.save(fname)

model6 = gensim.models.word2vec.Word2Vec(sentences, window = 2, size = 12, min_count = 5, workers = 4, iter = 80)

fname = "trained_model_80.txt"

# store the trained model
model6.save(fname)

model7 = gensim.models.word2vec.Word2Vec(sentences, window = 2, size = 12, min_count = 5, workers = 4, iter = 45)

fname = "trained_model_45.txt"

# store the trained model
model7.save(fname)

model8 = gensim.models.word2vec.Word2Vec(sentences, window = 2, size = 12, min_count = 5, workers = 4, iter = 40)

fname = "trained_model_40.txt"

# store the trained model
model8.save(fname)
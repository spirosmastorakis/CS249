# import modules & logging
import gensim, logging

# set up logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# input file
sentences = []

f = open("PaperAuthor.csv")
for line in f:
    print line
    sentences.append(line)

# convert to "multiword" sentences
bigram_transformer = gensim.models.Phrases(sentences)

# train word2vec on the two sentences
model = gensim.models.Word2Vec(bigram_transformer[sentences], size = 200, min_count = 1)

# redundant
# model.train(sentences)

# print model's accuracy based on test data
print model.accuracy('questions')

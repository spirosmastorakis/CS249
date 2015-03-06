# import modules & logging
import gensim, logging
#gensim.log_accuracy()

# set up logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# input file
# sentences = [ ['Athens', 'Greece'], ['Baghdad', 'Iraq'], ['data', 'test'] ]

sentences = gensim.models.word2vec.LineSentence('input')

#model.build_vocab([s.encode('utf-8').split() for s in sentences])

model = gensim.models.Word2Vec(sentences, window = 1, size=100, min_count=1, iter = 100)
#model.init_sims.log_accuracy(2)

# store the trained model
model.save('trained_model_100.txt')
#outfile = open('accuracy.txt', 'w');
# print model's accuracy based on test data
#model.accuracy('questions-words.txt')
#print model.most_similar_cosmul(positive ='1', )

#outfile.close()

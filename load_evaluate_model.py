# import modules & logging
import gensim, logging

# set up logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

fname = 'trained_model_100.txt'

# load stored model
model = gensim.models.Word2Vec.load(fname)
numbers = []
first_time = 0
last_added_element = ""
input = open('questions-words.txt', 'r')
output = open('output.txt', 'w')
for line in input:
    numbers = line.rstrip().split(" ")
    if (model.similarity(numbers[0], numbers[1]) >= 0.5):
        if (first_time == 0):
            first_time = first_time + 1
            last_added_element = numbers[0]
            output.write(last_added_element)
            output.write(",")
        if (numbers[0] != last_added_element):
            last_added_element = numbers[0]
            output.write("\n")
            output.write(last_added_element)
            output.write(",")
        print "correct"
        output.write(numbers[1])
        output.write(" ")
        continue
    print "incorrect"
output.close()


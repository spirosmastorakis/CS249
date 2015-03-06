# import modules & logging
import gensim, logging

# set up logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

fname = 'trained_model_50.txt'

# load stored model
model = gensim.models.Word2Vec.load(fname)
numbers = []
first_time = 0
last_added_element = ""
correct = 0
incorrect = 0
rows_added = 0
input = open('Result.txt', 'r')
output = open('output.csv', 'w')
output.write("AuthorId,PaperIds\n")
for line in input:
    numbers = line.rstrip().split(" ")
    if (first_time == 0):
        first_time = first_time + 1
        last_added_element = numbers[0]
        rows_added = rows_added + 1
        output.write(last_added_element)
        output.write(",")
        # output.write(" ")
    if (numbers[0] != last_added_element):
        last_added_element = numbers[0]
        output.write("\n")
        rows_added = rows_added + 1
        output.write(last_added_element)
        output.write(",")
        # output.write(" ")
    try:
        if (model.similarity(numbers[0], numbers[1]) >= -0.30):
            correct = correct + 1
            print "correct"
            output.write(numbers[1])
            output.write(" ")
            continue
        incorrect = incorrect + 1
        print "incorrect"
    except KeyError, e:
        continue
for i in range(rows_added, 2244):
    output.write("\n")
    output.write(str(i))
    output.write(",")
    print i
print "The number of correct answers is \n", correct
print "The number of incorrect answers is \n", incorrect
output.close()


import csv
import random

def sample_data(filename, out_filename, k):
    with open(out_filename, 'w', newline='') as fout:
        writer = csv.writer(fout, delimiter=',')
        with open(filename, newline='') as fin:
            reader = csv.reader(fin)
            for row in reader:
                if 'Id' in row[0]:
                    writer.writerow(row)
                else:
                    if random.randint(1, k) == 1:
                        writer.writerow(row)

def get_id_set(filename):
    id_set = set()
    with open(filename, newline='') as fin:
        reader = csv.reader(fin)
        for row in reader:
            if 'Id' not in row[0]:
                id_set.add(int(row[0]))
    return id_set

def sample_paper_author(filename, out_filename, k, author_set, paper_set):
    with open(out_filename, 'w', newline='') as fout:
        writer = csv.writer(fout, delimiter=',')
        with open(filename, newline='') as fin:
            reader = csv.reader(fin)
            for row in reader:
                if 'Id' in row[0]:
                    writer.writerow(row)
                else:
                    if int(row[0]) not in paper_set:
                        continue
                    if int(row[1]) not in author_set:
                        continue
                    if random.randint(1, k) == 1:
                        writer.writerow(row)

# sample_data('./Cleaned/Author.csv', 'Author_sample.csv', 10)
# sample_data('./Cleaned/Paper.csv', 'Paper_sample.csv', 10)
author_set = get_id_set('Author_sample.csv')
paper_set = get_id_set('Paper_sample.csv')
sample_paper_author('./Cleaned/PaperAuthor.csv', 'PaperAuthor_sample.csv', 10, author_set, paper_set)


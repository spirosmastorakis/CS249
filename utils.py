import csv
from db import Author
from db import Paper


class Utils(object):
    def __init__(self):
        # author_list is a list of Author, author_dict maps author_id to array index of author_list.
        self.author_list = []
        self.author_dict = dict()

        # paper_list is a list of Paper, paper_dict maps paper_id to array index of paper_list.
        self.paper_list = []
        self.paper_dict = dict()

        # Load databases: Author, Paper, PaperAuthor.
        self.load_author_data('./dataRev2/Author.csv')
        print("Load author data done...")

        self.load_paper_data('./dataRev2/Paper.csv')
        print("Load paper data done...")

        self.load_paper_author_data('./dataRev2/PaperAuthor.csv')
        print("Load paper-author data done...")

        self.load_non_ambiguous_paper('./non_ambiguous_paper_author.csv')
        print("Load non ambiguous data done...")

        # Load the training data
        self.load_train_data('./dataRev2/Train.csv')

    # Given author id, returns Author instance reference
    def _author_id2author(self, author_id):
        author_array_index = self.author_dict.get(author_id)
        if author_array_index is None:
            return None
        else:
            return self.author_list[author_array_index]

    # Given paper id, returns Paper instance reference
    def _paper_id2paper(self, paper_id):
        paper_array_index = self.paper_dict.get(paper_id)
        if paper_array_index is None:
            return None
        else:
            return self.paper_list[paper_array_index]

    # Load Author database
    def load_author_data(self, filename):
        array_index = 0
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'Id':
                    self.author_list.append(Author(row[0], row[1], row[2]))
                    self.author_dict[int(row[0])] = array_index
                    array_index += 1

    # Load Paper database
    def load_paper_data(self, filename):
        array_index = 0
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'Id':
                    self.paper_list.append(Paper(row[0], row[1], row[2], row[3], row[4], row[5]))
                    self.paper_dict[int(row[0])] = array_index
                    array_index += 1

    # Load PaperAuthor database
    def load_paper_author_data(self, filename):
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'PaperId':
                    paper_id = int(row[0])
                    author_id = int(row[1])

                    # TODO(@haochen): Now when the paper is not in the paper_list, we ignore it.
                    paper_array_index = self.paper_dict.get(paper_id)
                    if paper_array_index is None:
                        continue

                    author_array_index = self.author_dict.get(author_id)
                    if author_array_index is None:
                        continue

                    if author_array_index is not None:
                        self.author_list[author_array_index].add_candidate_paper(paper_id)
                    else:
                        self.author_dict[author_id] = len(self.author_list)
                        self.author_list.append(Author(row[1], row[2], row[3]))
                        self.author_list[-1].add_candidate_paper(paper_id)

                    if paper_array_index is not None:
                        self.paper_list[paper_array_index].add_candidate_author(author_id)

    def load_non_ambiguous_paper(self, filename):
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'Id':
                    author = self._author_id2author(int(row[0]))
                    for paper_id_str in row[1].split('|'):
                        if paper_id_str != '':
                            author.add_non_ambiguous_paper(int(paper_id_str))

    def get_all_last_name_of_authors(self, paper_id):
        paper = self._paper_id2paper(paper_id)
        if paper is None:
            return

        name_list = []
        for author_id in paper.candidate_authors:
            author = self._author_id2author(author_id)
            name_list.append(author.get_last_name())
        return name_list

    # Given author_id, find all the papers where the author is a non-ambiguous author.
    # Here, we define an author is a non-ambiguous author of paper p, if there doesn't
    # has other co-authors of the paper that has the same last name as the the author.
    # TODO(haochen): using last name is immature.
    def find_non_ambiguous_papers(self, author_id):
        author = self._author_id2author(author_id)
        if author is None:
            return []

        non_ambiguous_paper_list = []
        last_name = author.get_last_name()
        for p_id in author.candidate_papers:
            name_list = self.get_all_last_name_of_authors(p_id)
            if len([name for name in name_list if last_name == name]) == 1:
                # non-ambiguous
                non_ambiguous_paper_list.append(p_id)
        return non_ambiguous_paper_list

    def test_author(self):
        while 1:
            author_id = int(input('Author Id: '))
            author = self._author_id2author(author_id)
            if author is None:
                print("None")
            else:
                print(author)
                self.find_non_ambiguous_papers(author_id)

    def test_paper(self):
        while 1:
            paper_id = int(input('Paper Id: '))
            paper = self._paper_id2paper(paper_id)
            if paper is None:
                print("None")
            else:
                print(paper)
                self.get_all_last_name_of_authors(paper_id)

    def write_non_ambiguous_paper(self):
        with open('non_ambiguous_paper.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(["Id", "NonAmbiguousPapers"])
            for author in self.author_list:
                author_id = int(author.id)
                print(author_id)
                # print(self.find_non_ambiguous_papers(author_id))
                writer.writerow([str(author_id),
                                 '|'.join([str(x) for x in self.find_non_ambiguous_papers(author_id)])])

    def get_feature_paper(self, paper):
        word_list = []
        for word in paper.title.split():
            if word != '':
                word_list.append(word)
        for word in paper.keywords.split('|'):
            if word != '':
                word_list.append(word)
        return word_list

    def get_feature_author(self, author):
        word_list = []
        for paper_id in author.non_ambiguous_paper_ids:
            paper = self._paper_id2paper(paper_id)
            if paper is not None:
                word_list.extend(self.get_feature_paper(paper))
        return word_list

    def get_feature_vector(self, author_id, paper_id):
        feature_vector = []

        author = self._author_id2author(author_id)
        paper = self._paper_id2paper(paper_id)
        if author is None or paper is None:
            return None

        # print("Author: ", author)
        # print("Author.non_ambiguous_paper_ids: ", author.non_ambiguous_paper_ids)

        # print("Paper: ", paper)

        # 1. tf-idf score of matching keywords of p and a
        paper_str = self.get_feature_paper(paper)
        author_str = self.get_feature_author(author)

        # print(author_str)
        # print(paper_str)

        score = []
        for word in paper_str:
            num_tot = 0
            for x in author_str:
                if x == word:
                    num_tot += 1
            if num_tot > 0:
                score.append(float(num_tot) / len(author_str))

        for num in range(len(score), 5):
            score.append(0.0)
        score.sort(reverse=True)
        for num in range(0, 5):
            feature_vector.append(score[num])

        # 3. the number of co-author of p that has the same affiliation with a
        num_with_same_affiliation = 0
        for new_author_id in paper.candidate_authors:
            new_author = self._author_id2author(new_author_id)
            if new_author is not None and new_author.affiliation == author.affiliation:
                if new_author != '':
                    num_with_same_affiliation += 1
        num_with_same_affiliation -= 1
        if num_with_same_affiliation < 0:
            num_with_same_affiliation = 0
        feature_vector.append(num_with_same_affiliation)

        # 4. the number of candidate authors of p
        feature_vector.append(paper.num_candidate_authors)

        # 5. the number of candidate authors of p having the same last name as a
        num_candidate = 0
        for new_author_id in paper.candidate_authors:
            new_author = self._author_id2author(new_author_id)
            if new_author is not None and new_author.get_last_name() == author.get_last_name():
                num_candidate += 1
        feature_vector.append(num_candidate)

        # 6. the number of candidate papers of a
        feature_vector.append(author.num_candidate_papers)

        return feature_vector

    def test_feature_vector(self):
        while 1:
            author_id = int(input("Author Id: "))
            paper_id = int(input("Paper Id: "))
            print(self.get_feature_vector(author_id, paper_id))

    def get_dictionary(self):
        word_dict = dict()
        for paper in self.paper_list:
            for word in paper.title.split():
                if word_dict.get(word) is None:
                    word_dict[word] = 1
                else:
                    word_dict[word] += 1
            for word in paper.keywords.split('|'):
                if word_dict.get(word) is None:
                    word_dict[word] = 1
                else:
                    word_dict[word] += 1
        return word_dict

    def test_dictionary(self):
        word_dict = self.get_dictionary()
        while 1:
            st = input("Word")
            if word_dict.get(st) is None:
                print("None")
            else:
                print(word_dict[st])

    def load_train_data(self, filename):
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'AuthorId':
                    author_id = int(row[0])
                    for confirm_paper in row[1].split(' '):
                        if confirm_paper is '':
                            break
                        paper_id = int(confirm_paper)
                        print(self.get_feature_vector(author_id, paper_id))

                    for deleted_paper in row[2].split(' '):
                        if deleted_paper is '':
                            break
                        paper_id = int(deleted_paper)
                        print(self.get_feature_vector(author_id, paper_id))

                    wc = input("input any key to continue")

if __name__ == "__main__":
    utils = Utils()
    utils.test_feature_vector()

    #utils.test_dictionary()
    # utils.write_non_ambiguous_paper()
    # utils.test_paper()
    # utils.test_author()

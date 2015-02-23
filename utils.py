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
        self.load_paper_data('./dataRev2/Paper.csv')
        self.load_paper_author_data('./dataRev2/PaperAuthor.csv')

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
                    if author_array_index is not None:
                        self.author_list[author_array_index].add_candidate_paper(paper_id)
                    else:
                        self.author_dict[author_id] = len(self.author_list)
                        self.author_list.append(Author(row[1], row[2], row[3]))
                        self.author_list[-1].add_candidate_paper(paper_id)

                    if paper_array_index is not None:
                        self.paper_list[paper_array_index].add_candidate_author(author_id)

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

if __name__ == "__main__":
    utils = Utils()
    utils.write_non_ambiguous_paper()
    # utils.test_paper()
    # utils.test_author()

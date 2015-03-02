import csv
import jellyfish
from db import Author
from db import Paper

stoplist = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

class Utils(object):
    def __init__(self):
        # author_list is a list of Author, author_dict maps author_id to array index of author_list.
        self.author_list = []
        self.author_dict = dict()

        # paper_list is a list of Paper, paper_dict maps paper_id to array index of paper_list.
        self.paper_list = []
        self.paper_dict = dict()


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
                    author_id = int(row[0])
                    name = row[1].lower()
                    affiliation = row[2].lower()
                    if len(affiliation) > 0:
                        if affiliation[0] == '"' and affiliation[-1] == '"':
                            affiliation = affiliation[1:-1]
                    affiliation = " ".join([w for w in affiliation.replace(",",' ').replace(";", ' ').split() if w not in stoplist])
                
                    self.author_list.append(Author(author_id, name, affiliation))
                    self.author_dict[author_id] = array_index
                    array_index += 1

    # Load Paper database
    def load_paper_data(self, filename):
        array_index = 0
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'Id':
                    paper_id = int(row[0])

                    title = row[1].lower()
                    if len(title) > 0:
                        if title[0] == '"' and title[-1] == '"':
                            title = title[1:-1]
                        title = " ".join([w for w in title.split() if w not in stoplist])

                    year = int(row[2])
                    if year <= 1000 or year > 2015:
                        year = 0
                    
                    conference_id = int(row[3])
                    journal_id = int(row[4])
                    keywords = row[5]
                    keywords = [w for w in keywords.lower().replace("|", ' ').replace(',', ' ').split()]

                    self.paper_list.append(Paper(paper_id, title, year, conference_id, 
                                                 journal_id, keywords))
                    self.paper_dict[paper_id] = array_index
                    array_index += 1

    # Load PaperAuthor database
    def load_paper_author_data(self, filename):
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'PaperId':
                    paper_id = int(row[0])
                    author_id = int(row[1])
                    if paper_id not in self.paper_dict:
                        continue

                    name = row[2].lower()
                    affiliation = row[3].lower()
                    if len(affiliation) > 0:
                        if affiliation[0] == '"' and affiliation[-1] == '"':
                            affiliation = affiliation[1:-1]
                        affiliation = " ".join([w for w in affiliation.replace(",",' ').replace(";", ' ').split() if w not in stoplist])

                    # TODO(@haochen): Now when the paper is not in the paper_list, we ignore it.
                    if paper_id not in self.paper_dict:
                        continue
                    paper = self.paper_list[self.paper_dict[paper_id]]
                    paper.add_candidate_author((author_id, name, affiliation))

                    if author_id in self.author_dict:
                        author = self.author_list[self.author_dict[author_id]]
                        author.add_candidate_paper(paper_id)

    def get_all_last_name_of_authors(self, paper_id):
        paper = self._paper_id2paper(paper_id)
        if paper is None:
            return

        name_list = []
        for author_id in paper.candidate_authors:
            author = self._author_id2author(author_id)
            name_list.append(author.get_last_name())
        return name_list

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

    def features_author_paper(self, author_id, paper_id):
        feature_vector = []
        feature_vector.extend(self.features_author_profile(author_id, paper_id))
        feature_vector.extend(self.features_coauthor_name_matching(author_id, paper_id))
        feature_vector.extend(self.feature_time(author_id, paper_id))
        feature_vector.extend(self.feature_bibliographic_network(author_id, paper_id))
        return feature_vector

    def test_paper_author(self):
        while 1:
            author_id = int(input("Author Id: "))
            paper_id = int(input("Paper Id: "))

            author = self._author_id2author(author_id)
            paper = self._paper_id2paper(paper_id)

            if author is None:
                print("Author: None")
            else:
                print("Author ", author)

            if paper is None:
                print("Paper: None")
            else:
                print("Paper ", paper)

            print("features_author_profile: ", self.features_author_profile(author_id, paper_id))
            print("features_coauthor_name_matching: ", self.features_coauthor_name_matching(author_id, paper_id))
            print("features_year: ", self.feature_time(author_id, paper_id))
            print("features_bibliographic network: ", self.feature_bibliographic_network(author_id, paper_id))


            feature_vector = []
            feature_vector.extend(self.features_author_profile(author_id, paper_id))
            feature_vector.extend(self.features_coauthor_name_matching(author_id, paper_id))
            feature_vector.extend(self.feature_time(author_id, paper_id))
            feature_vector.extend(self.feature_bibliographic_network(author_id, paper_id))
            print("OVER ALL: ", feature_vector)

    def features_author_profile(self, author_id, paper_id):
        # the levenshtein distance between the names of the target author in Author.csv
        # and PaperAuthor.csv
        author = self._author_id2author(author_id)
        paper = self._paper_id2paper(paper_id)

        author_name = author.name
        author_affiliation = author.affiliation

        name_distance = []
        affiliation_distance = []

        for uid, name, affiliation in paper.candidate_authors:
            if int(uid) == int(author_id):
                continue

            # print("candidate: ", name, " : ", affiliation)
            if len(name) > 0:
                name_distance.append(jellyfish.levenshtein_distance(author_name, name))
            if len(author_affiliation) > 0 and len(affiliation) > 0:
                affiliation_distance.append(jellyfish.levenshtein_distance(author_affiliation, affiliation))

        return [max(name_distance) if len(name_distance) > 0 else 0.5,
                max(affiliation_distance) if len(affiliation_distance) > 0 else 0.5]

    def features_coauthor_name_matching(self, author_id, paper_id):
        # the maximum Jaro distances between the target author's name and each coauthor's name.
        author = self._author_id2author(author_id)
        paper = self._paper_id2paper(paper_id)
        author_name = author.name
        author_last_name = author.get_last_name()
        author_affiliation = author.affiliation

        coauthor_name_jaro_dist = []
        coauthor_lastname_jaro_dist = []
        coauthor_name_jaro_dist_ig = []
        coauthor_lastname_leve_dist_ig = []

        coauthor_affi_jaro_dist = []
        coauthor_affi_leve_dist = []

        for uid, name, affiliation in paper.candidate_authors:
            if int(uid) == int(author_id):
                continue

            # print("candidate: ", name, " : ", affiliation)
            if len(name) > 0:
                coauthor_name_jaro_dist.append(jellyfish.jaro_distance(author_name, name))
                coauthor_lastname_jaro_dist.append(
                    jellyfish.jaro_distance(author_last_name, Author.get_last_name_static(name)))

                if len(author_affiliation) > 0 and len(affiliation) > 0 and author_affiliation != affiliation:
                    coauthor_name_jaro_dist_ig.append(jellyfish.jaro_distance(author_name, name))
                    coauthor_lastname_leve_dist_ig.append(
                        jellyfish.levenshtein_distance(author_last_name, Author.get_last_name_static(name)))

            if len(author_affiliation) > 0 and len(affiliation) > 0:
                coauthor_affi_jaro_dist.append(jellyfish.jaro_distance(author_affiliation, affiliation))
                coauthor_affi_leve_dist.append(jellyfish.levenshtein_distance(author_affiliation, affiliation))

        return [max(coauthor_name_jaro_dist) if len(coauthor_name_jaro_dist) > 0 else 0.5,
                max(coauthor_lastname_jaro_dist) if len(coauthor_lastname_jaro_dist) > 0 else 0.5,
                max(coauthor_name_jaro_dist_ig) if len(coauthor_name_jaro_dist_ig) > 0 else 0.5,
                min(coauthor_lastname_leve_dist_ig) if len(coauthor_lastname_leve_dist_ig) > 0 else 0.5,
                max(coauthor_affi_jaro_dist) if len(coauthor_affi_jaro_dist) > 0 else 0.5,
                min(coauthor_affi_leve_dist) if len(coauthor_affi_leve_dist) > 0 else 0.5]

    def feature_bibliographic_network(self, author_id, paper_id):
        author = self._author_id2author(author_id)
        paper = self._paper_id2paper(paper_id)

        coauthors_id = []
        for uid, name, affiliation in paper.candidate_authors:
            if int(uid) == int(author_id):
                continue
            coauthors_id.append(int(uid))
        number_coauthors = len(set(coauthors_id))

        num_conference = 0
        num_journal = 0
        for pid in author.candidate_papers:
            paper_related = self._paper_id2paper(int(pid))
            if len(paper_related.conference_id) > 0 and paper_related.conference_id == paper.conference_id:
                num_conference += 1
            if len(paper_related.journal_id) > 0 and paper_related.journal_id == paper.journal_id:
                num_journal += 1

        return [author.num_candidate_papers, number_coauthors, num_conference, num_journal]

    def feature_time(self, author_id, paper_id):
        author = self._author_id2author(author_id)
        paper = self._paper_id2paper(paper_id)

        earliest_year = 2100
        latest_year = 0
        for pid in author.candidate_papers:
            paper_related = self._paper_id2paper(int(pid))
            if len(paper_related.year) > 2:
                earliest_year = min(int(paper_related.year), earliest_year)
                latest_year = max(int(paper_related.year), latest_year)

        publication_year = int(paper.year) if len(paper.year) > 2 else 0
        indicator_missing_year = 1 if publication_year > 0 else 0

        return [earliest_year, latest_year, publication_year, indicator_missing_year]


class FeatureGenerator:
    def __init__(self):
        self.utils = Utils()
        # self.test()

    def convert_train_data(self, filename):
        data_list = []

        count = 0
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'AuthorId':
                    count += 1
                    print("count", count)
                    author_id = int(row[0])
                    for pid in row[1].split(' '):
                        item = self.utils.features_author_paper(author_id, int(pid))
                        item.append(1)
                        data_list.append(item)

                    for pid in row[2].split(' '):
                        item = self.utils.features_author_paper(author_id, int(pid))
                        item.append(-1)
                        data_list.append(item)

        with open('features_train.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            for data in data_list:
                writer.writerow(data)

if __name__ == "__main__":
    utils = Utils()
    
    utils.load_author_data('./Cleaned/Author.csv')
    print("Load author data done...")

    utils.load_paper_data('./Cleaned/Paper.csv')
    print("Load paper data done...")

    utils.load_paper_author_data('./Cleaned/PaperAuthor.csv')
    print("Load paper-author data done...")

    utils.test_paper_author()

    # feature_generator = FeatureGenerator()
    # feature_generator.convert_train_data('./dataRev2/Train.csv')

    #utils.test_dictionary()
    # utils.write_non_ambiguous_paper()
    # utils.test_paper()
    # utils.test_author()

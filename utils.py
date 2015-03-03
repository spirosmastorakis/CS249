import csv
import jellyfish
import difflib
from db import Author
from db import Paper

stoplist = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

def get_last_name(st):
    l_st = st.split()
    if len(l_st) == 0:
        return ''
    return l_st[-1]

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

    # Returns the coauthor_id set of a paper
    def _coauthor_id_set_of_paper_id(self, paper_id):
        coauthors = set()
        paper = self._paper_id2paper(paper_id)
        if paper is None:
            return coauthors
        for aid, name, affiliation in paper.candidate_authors:
            coauthors.add(aid)
        return coauthors

    # Returns set of distinct keywords in the author's papers
    def _distinct_keywords_of_author(self, author_id):
        keywords = set()
        author = self._author_id2author(author_id) 
        if author is None:
            return keywords

        for pid in author.candidate_papers:
            paper = self._paper_id2paper(pid)
            if paper is not None:
                keywords &= paper.keywords
        return keywords

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

    def feature_generate(self, paper_id, author_id):
        author = self._author_id2author(author_id)
        paper = self._paper_id2paper(paper_id)
        # print(author)
        # print(paper)
        if author is None or paper is None:
            return None

        feature = []

        # 1. number of paper in the same journal/conference
        num_paper_with_same_journal = 0
        num_paper_with_same_conference = 0
        for pid in author.candidate_papers:
            this_paper = self._paper_id2paper(pid)
            if this_paper is None:
                continue
            if paper.journal_id > 0 and this_paper.journal_id == paper.journal_id:
                num_paper_with_same_journal += 1
            if paper.conference_id > 0 and this_paper.conference_id == paper.conference_id:
                num_paper_with_same_conference += 1
        feature.append(max(num_paper_with_same_journal, num_paper_with_same_conference))

        # 2. count of all papers of the author
        feature.append(len(author.candidate_papers))

        # 3. count of all distinct keywords in the author's papers
        keywords_all_papers = self._distinct_keywords_of_author(author_id)
        feature.append(len(keywords_all_papers))

        # 4. count of keywords in the paper
        feature.append(len(paper.keywords))

        # 5. farest distance with name between author.csv and paperauthor.csv
        ratio = list()
        for aid, name, affiliation in paper.candidate_authors:
            if aid == author_id:
                if len(name) == 0 and len(author.name) == 0:
                    ratio.append(0.5)
                else:
                    ratio.append(difflib.SequenceMatcher(None, author.name, name).ratio())
        if len(ratio) == 0:
            feature.append(-1)
        else:
            feature.append(min(ratio))

        # 6. 7 farest distance (ratio and levenshitein_dist) with affiliation between 
        # author.csv and paperauthor.csv
        ratio = list()
        levenshteindistance = list()
        for aid, name, affiliation in paper.candidate_authors:
            if aid == author_id:
                if len(affiliation) == 0 and len(author.affiliation) == 0:
                    ratio.append(0.5)
                    levenshteindistance.append(30)
                else:
                    ratio.append(difflib.SequenceMatcher(None, author.affiliation, affiliation).ratio())
                    levenshteindistance.append(jellyfish.levenshtein_distance(author.affiliation,
                                                                              affiliation))
        if len(ratio) > 0:
            feature.append(min(ratio))
            feature.append(max(levenshteindistance))
        else:
            feature.append(-1)
            feature.append(-1)

        # 8. number of coauthor with same last name
        # 9. number of coauthor with same affiliation
        number_coauthors_with_same_last_name = 0
        number_coauthors_with_same_affiliation = 0
        for aid, name, affiliation in paper.candidate_authors:
            if aid != author_id:
                if get_last_name(name) == get_last_name(author.name):
                    number_coauthors_with_same_last_name += 1
                if len(author.affiliation) > 0 and affiliation == author.affiliation:
                    number_coauthors_with_same_affiliation += 1
                elif len(author.affiliation) > 0 and aid in self.author_dict:
                    coauthor = self._author_id2author(aid)
                    if coauthor is not None and coauthor.affiliation == author.affiliation:
                        number_coauthors_with_same_affiliation += 1
        feature.append(number_coauthors_with_same_last_name)
        feature.append(number_coauthors_with_same_affiliation)

        # 10. number of coauthro:
        coauthors_paper = self._coauthor_id_set_of_paper_id(paper_id)
        feature.append(len(coauthors_paper))

        # 11. ratio of number of papers that has intersection coauthor with the paper
        # 12. the number of papers
        # 13. the number of papers with thte same coauthors
        # 14. the number of author's coauthros
        all_coauthors_of_the_author = set()
        all_coauthors_of_the_author |= coauthors_paper

        num_papers_with_intersection_coauthor = 0
        for pid in author.candidate_papers:
            if pid != paper_id:
                this_paper_coauthors = self._coauthor_id_set_of_paper_id(pid)
                all_coauthors_of_the_author |= this_paper_coauthors
                if len(this_paper_coauthors & coauthors_paper) > 1:
                    num_papers_with_intersection_coauthor += 1
        feature.append(float(num_papers_with_intersection_coauthor) / float(len(author.candidate_papers)))
        feature.append(len(set(author.candidate_papers)))
        feature.append(num_papers_with_intersection_coauthor)
        feature.append(len(all_coauthors_of_the_author))

        # 15. max number of papers writen by the author and another coauthor. 
        # 16. max ratio of papers writen by the author and another coauthro.
        overlap = list()
        intersect_num = list()
        for coauthor_id in coauthors_paper:
            if coauthor_id == author_id or coauthor_id not in self.author_dict:
                continue
            coauthor = self._author_id2author(coauthor_id)

            union = len(set(coauthor.candidate_papers) | set(author.candidate_papers))
            intersect = len(set(coauthor.candidate_papers) & set(author.candidate_papers))
            intersect_num.append(intersect)
            overlap.append(float(intersect) / float(union))
        if len(overlap) > 0:
            feature.append(max(overlap))
            feature.append(max(intersect_num))
        else:
            feature.append(-1)
            feature.append(-1)

        # 17. farestyear
        # 18. number of author's papers of the same year 
        fearestyear = 0
        num_same_year_papers = 0
        for pid in author.candidate_papers:
            if pid != paper_id:
                other_paper = self._paper_id2paper(pid)
                if other_paper is not None and other_paper.year > 0:
                    fearestyear = max(fearestyear, abs(other_paper.year - paper.year)) 
                if other_paper is not None and other_paper.year > 0 and other_paper.year == paper.year:
                    num_same_year_papers += 1
        if paper.year > 0:
            feature.append(fearestyear)
        else:
            feature.append(-1)
        feature.append(num_same_year_papers)

        # 20. 21 distance of title of other papers's title
        # 22. similarity rate of keywords of the paper between other papers
        # 23. the number of keywords shows in other paper
        jarodistance = list()
        levenshteindistance = list()
        keywords_intersect_rate = list()
        num_papers_with_same_keyword = 0

        for pid in author.candidate_papers:
            if pid != paper_id:
                other_paper = self._paper_id2paper(pid)
                if other_paper is None:
                    continue
                if len(other_paper.title) == 0 and len(paper.title) == 0:
                    jarodistance.append(0.5)
                    levenshteindistance.append(50)
                else:
                    jarodistance.append(jellyfish.jaro_distance(paper.title, other_paper.title))
                    levenshteindistance.append(jellyfish.levenshtein_distance(paper.title, other_paper.title))
                intersect_keywords_len = len(paper.keywords & other_paper.keywords)
                union_keywords_len = len(paper.keywords | other_paper.keywords)
                if union_keywords_len > 0:
                    keywords_intersect_rate.append(float(intersect_keywords_len) / float(union_keywords_len))
                if intersect_keywords_len > 0:
                    num_papers_with_same_keyword += 1

        if len(jarodistance) > 0:
            feature.append(max(jarodistance))
            feature.append(min(levenshteindistance))
        else:
            feature.append(-1)
            feature.append(-1)
        if len(keywords_intersect_rate) > 0:
            feature.append(max(keywords_intersect_rate))
        else:
            feature.append(-1)
        feature.append(num_papers_with_same_keyword)


        # 24, 25. affiliation similarity with coauthor in other paper
        jarodistance = list()
        levenshteindistance = list()
        for otherauthor_id in paper.candidate_authors:
            if otherauthor_id != author_id:
                otherauthor = self._author_id2author(otherauthor_id)
                if otherauthor is None:
                    continue

                if len(otherauthor.affiliation) == 0 and len(author.affiliation) == 0:
                    jarodistance.append(0.5)
                    levenshteindistance.append(25)
                else:
                    jarodistance.append(jellyfish.jaro_distance(otherauthor.affiliation, author.affiliation))
                    levenshteindistance.append(jellyfish.levenshtein_distance(otherauthor.affiliation, author.affiliation))
        if len(jarodistance) > 0:
            feature.append(max(jarodistance))
            feature.append(max(levenshteindistance))
        else:
            feature.append(-1)
            feature.append(-1)

        return feature


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

            print(self.feature_generate(paper_id, author_id))


class FeatureGenerator:
    def __init__(self):
        self.utils = Utils()
        
        self.utils.load_author_data('./Cleaned/Author.csv')
        print("Load author data done...")

        self.utils.load_paper_data('./Cleaned/Paper.csv')
        print("Load paper data done...")

        self.utils.load_paper_author_data('./Cleaned/PaperAuthor.csv')
        print("Load paper-author data done...")
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
                        item = self.utils.feature_generate(int(pid), author_id)
                        item.append(1)
                        data_list.append(item)

                    for pid in row[2].split(' '):
                        item = self.utils.feature_generate(int(pid), author_id)
                        item.append(-1)
                        data_list.append(item)

        with open('features_train_3.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            for data in data_list:
                writer.writerow(data)


if __name__ == "__main__":
    """
    utils = Utils()
    
    utils.load_author_data('Author_sample.csv')
    #utils.load_author_data('./Cleaned/Author.csv')
    print("Load author data done...")

    utils.load_paper_data('Paper_sample.csv')
    #utils.load_paper_data('./Cleaned/Paper.csv')
    print("Load paper data done...")

    utils.load_paper_author_data('PaperAuthor_sample.csv')
    #utils.load_paper_author_data('./Cleaned/PaperAuthor.csv')
    print("Load paper-author data done...")

    utils.test_paper_author()
    """

    feature_generator = FeatureGenerator()
    feature_generator.convert_train_data('./dataRev2/Train.csv')
    
    #utils.test_dictionary()
    # utils.write_non_ambiguous_paper()
    # utils.test_paper()
    # utils.test_author()

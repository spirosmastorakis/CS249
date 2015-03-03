import csv


class Author:
    def __init__(self, name, affiliation):
        self.name = name
        self.affiliation = affiliation
    
    def __str__(self):
        return ','.join([self.name, self.affiliation])

class Paper:
    def __init__(self, title, year, c_id, j_id, keywords):
        self.title = title
        self.year = year
        self.conference_id = c_id
        self.journal_id = j_id
        self.keywords = keywords

    def __str__(self):
        return ','.join([self.title, str(self.year), str(self.conference_id),
                         str(self.journal_id), str(self.keywords)])

stoplist = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

class PADataSet:
    def __init__(self):
        # Author.csv
        self.author_set = dict()

        # Paper.csv
        self.paper_set = dict()

        self.paper_author = dict()
        self.author_paper = dict()

        self.paperauthor_namelist = dict()
        self.paperauthor_affiliationlist = dict()

    def read_author_csv(self, filename):
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == 'Id':
                    continue
                author_id = int(row[0])
                name = row[1].lower()
                affiliation = row[2].lower()

                if len(affiliation) > 0:
                    if affiliation[0] == '"' and affiliation[-1] == '"':
                        affiliation = affiliation[1:-1]
                    affiliation = " ".join([w for w in affiliation.replace(",",' ').replace(";", ' ').split() if w not in stoplist])
                

                self.author_set[author_id] = Author(name, affiliation)

    def read_paper_csv(self, filename):
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == 'Id':
                    continue
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


                self.paper_set[paper_id] = Paper(title, year, conference_id, journal_id, keywords)

    def read_paper_author_csv(self, filename):
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == 'PaperId':
                    continue
                paper_id = int(row[0])
                author_id = int(row[1])
                if paper_id not in self.paper_set:
                    continue

                name = row[2].lower()
                affiliation = row[3].lower()
                if len(affiliation) > 0:
                    if affiliation[0] == '"' and affiliation[-1] == '"':
                        affiliation = affiliation[1:-1]
                    affiliation = " ".join([w for w in affiliation.replace(",",' ').replace(";", ' ').split() if w not in stoplist])

                if paper_id not in self.paper_author:
                    self.paper_author[paper_id] = set()
                self.paper_author[paper_id].add(author_id)
                if author_id not in self.author_paper:
                    self.author_paper[author_id] = set()
                self.author_paper[author_id].add(paper_id)

                if paper_id not in self.paperauthor_namelist:
                    self.paperauthor_namelist[paper_id] = dict()
                if author_id not in self.paperauthor_namelist[paper_id]:
                    self.paperauthor_namelist[paper_id][author_id] = list()
                self.paperauthor_namelist[paper_id][author_id].append(name)

                if paper_id not in self.paperauthor_affiliationlist:
                    self.paperauthor_affiliationlist[paper_id] = dict()
                if author_id not in self.paperauthor_affiliationlist[paper_id]:
                    self.paperauthor_affiliationlist[paper_id][author_id] = list()
                self.paperauthor_affiliationlist[paper_id][author_id].append(affiliation)
                

    def feature_generate(self, author_id, paper_id):
        author = self.author_set[author_id]
        paper = self.paper_set[paper_id]

        feature = []

        # 1. number of papers the author published in the conference/journal
        num_papers_in_same_conference = 0
        num_papers_in_same_journal = 0
        for pid in self.author_paper[author_id]:
            if pid in self.paper_set:
                this_paper = self.paper_set[pid]
                if this_paper.conference_id == paper.conference_id:
                    num_papers_in_same_conference += 1
                if this_paper.journal_id == paper.journal_id:
                    num_papers_in_same_journal += 1
        feature.append(num_papers_in_same_conference)
        feature.append(num_papers_in_same_journal)

        # 2. number of publication of the author:
        if author_id in self.author_paper:
            feature.append(len(self.author_paper[author_id]))
        else:
            feature.append(-1)

        # 3. number of coauthor:
        if paper_id in self.paper_author:
            feature.append(len(self.paper_author[paper_id]))
        else:
            feature.append(-1)

        # 4.
        return feature


    def test_read_data(self):
        while 1:
            author_id = int(input("Author Id: "))
            paper_id = int(input("Paper Id: "))
            if author_id in self.author_set:
                print(self.author_set[author_id])
            else:
                print("None")

            if author_id in self.author_paper:
                print(self.author_paper[author_id])
            else:
                print("None")

            if paper_id in self.paper_set:
                print(self.paper_set[paper_id])
            else:
                print("None")

            if paper_id in self.paper_author:
                print(self.paper_author[paper_id])
            else:
                print("None")

if __name__ == "__main__":
    data = PADataSet()
    data.read_author_csv('./Cleaned/Author.csv')
    print("load author done")
    data.read_paper_csv('./Cleaned/Paper.csv')
    print("load paper done")
    data.read_paper_author_csv('./Cleaned/PaperAuthor.csv')
    print("load paper author done")
    data.test_read_data()



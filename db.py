

class Author(object):
    def __init__(self, id, name, affiliation):
        self.id = id
        self.name = name
        self.affiliation = affiliation
        self.num_candidate_papers = 0
        self.candidate_papers = []

    def __str__(self):
        return ', '.join([str(self.id), self.name, self.affiliation, str(self.num_candidate_papers)])

    def add_candidate_paper(self, paper_id):
        self.candidate_papers.append(paper_id)
        self.num_candidate_papers += 1

    def get_last_name(self):
        return self.name.split(' ')[-1]

    @staticmethod
    def get_last_name_static(name):
        return name.split(' ')[-1]


class Paper(object):
    def __init__(self, id, title, year, conference_id, journal_id, keywords):
        self.id = id
        self.title = title
        self.year = year
        self.conference_id = conference_id
        self.journal_id = journal_id
        self.keywords = keywords
        self.candidate_authors = []
        self.num_candidate_authors = 0

    def __str__(self):
        return ', '.join([str(self.id), self.title, str(self.year),
                          str(self.conference_id), str(self.journal_id), 
                          str(self.keywords),
                          str(self.num_candidate_authors)])

    def add_candidate_author(self, author_info):
        # author_info = (author_id, name, affiliation)
        self.candidate_authors.append(author_info)
        self.num_candidate_authors += 1


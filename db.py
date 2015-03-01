def remove_stopping_word(st):
    stopwords = ['a', 'an', 'is', 'are', 'the', 'of', 'at', 'in', 'on', 'out', 'with', 'one', 'for', 'and', 'or']
    return ' '.join([w for w in st.lower().split() if w not in stopwords])


class Author(object):
    def __init__(self, id, name, affiliation):
        self.id = id
        self.name = name
        self.affiliation = affiliation


        self.num_candidate_papers = 0
        self.candidate_papers = []
        self.non_ambiguous_paper_ids = []

    def __str__(self):
        return ', '.join([self.id, self.name, self.affiliation, str(self.num_candidate_papers)])

    def add_candidate_paper(self, paper_id):
        self.candidate_papers.append(paper_id)
        self.num_candidate_papers += 1

    def get_last_name(self):
        return self.name.split(' ')[-1]

    def add_non_ambiguous_paper(self, paper_id):
        self.non_ambiguous_paper_ids.append(paper_id)


class Paper(object):
    def __init__(self, id, title, year, conference_id, journal_id, keywords):
        self.id = id
        self.title = remove_stopping_word(title)
        self.year = year
        self.conference_id = conference_id
        self.journal_id = journal_id
        self.keywords = keywords
        self.candidate_authors = []
        self.num_candidate_authors = 0

    def __str__(self):
        return ', '.join([self.id, self.title, self.year,
                          self.conference_id, self.journal_id, self.keywords,
                          str(self.num_candidate_authors)])

    def add_candidate_author(self, author_id):
        self.candidate_authors.append(author_id)
        self.num_candidate_authors += 1


class PaperAuthor(object):
    def __init__(self, paper_id, author_id, name, affiliation):
        self.paper_id = paper_id
        self.author_id = author_id
        self.name = name
        self.affiliation = affiliation

    def __str__(self):
        return ', '.join([self.paper_id, self.author_id, self.name, self.affiliation])

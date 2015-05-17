"""
    Class definition of Sentence - a data structure that holds the words, the
    grammatical information and annotation content of a single sentence.
"""

class Sentence:
    # TODO? Index dependencies to speed up fetching them

    def __init__(self):
        self.lemmas = []
        self.words = []
        self.pos = []
        self.dependencies = []
        self.annotations = []
        self.offsets = []

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        string = ""
        for i in xrange(len(self.words)):
            string += self.words[i]
            if self.annotations[i] != None:
                string += "-"+self.annotations[i]
            string += " "
        return string+"\n"

    def get_dependencies_of(self, index):
        dependencies = []
        for dependency in self.dependencies:
            if dependency.governor == index:
                dependencies.append(dependency)
        return dependencies

    def get_governor_of(self, index):
     dependencies = []
     for dependency in self.dependencies:
       if dependency.dependent == index:
         dependencies.append(dependency)
     return dependencies


    def lemma_at(self, index):
      return self.lemmas[index]

class Dependency:

    def __init__(self, dep_type, governor, dependent):
        self.dep_type = dep_type
        self.governor = governor
        self.dependent = dependent

class Element():
    def __init__(self, identifier, name, symbol):
        self.identifier = identifier
        self.name = name
        self.symbol = symbol

        self.metabolites = []

    def add_compound(self, compound):
        if compound not in self.metabolites:
            self.metabolites.append(compound)

    def __repr__(self):
        return '<{0} {1!r}>'.format(self.__class__.__name__,
                                    (self.identifier, self.name, self.symbol))

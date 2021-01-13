fisu_link = "https://ps2.fisu.pw/player/?name="

class Planetman:

    def __init__(self, name, role):

        self.name = name
        self.fisu = fisu_link + name
        self.role = role

    def __cmp__(self, other):

        if self.name == other:
            return 0
        else:
            return 1

    def __repr__(self):

        return repr(self.__dict__)

    def __str__(self):

        return str(self.__dict__)

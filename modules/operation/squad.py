from .planetman import Planetman

class Squad:

    def __init__(self, sl=None, fl=None, composition=None):

        self.sl = sl
        self.fl = fl
        self.composition = composition
        self.members = []
        self.capacity = 12

    def __str__(self):

        return str(self.__dict__)

    def __repr__(self):

        return repr(self.__dict__)

    def add(self, name, role):

        '''
        Checks if the composition of the squad will allow the adition
        of the new squad member. Should composition be undefined, it is caught
        by the except TypeError: statement'
        '''

        try:
            if self.check_for_space(role) is False:
                self.composition[role] -= 1
            else:
                raise SquadCapacity
        except KeyError:
            raise SquadRole
        except TypeError:
            pass

        '''
        Checks if name is already in self.members. If it is, it will
        remove the member before readding
        '''

        for index, member in enumerate(self.members):
            if member.name == name:
                del self.members[index]

        self.members.append(Planetman(name, role))

    def check_for_space(self, role):

        try:
            return self.composition[role] < 1
        except KeyError:
            return False

    def remove(self, name):

        '''
        Iterates through self.members (List) looking for any Planetman 
        object with the Planetman.name as name and removes from the members
        list
        '''

        for index, member in enumerate(self.members):
            if member.name == name:
                try:
                    self.composition[member.role] += 1
                except:
                    pass
                del self.members[index]

        '''
        There are instances where name also equals Squad.sl or Squad.fl
        In this instance, Squad.sl or Squad.fl should also be removed
        '''

        if self.sl == name:
            self.sl = None

        if self.fl == name:
            self.fl = None

class SquadError(Exception):

    pass

class SquadExists(SquadError):

    pass

class SquadCapacity(SquadError):

    pass

class SquadRole(SquadError):

    pass

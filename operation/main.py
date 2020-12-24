from datetime import datetime

from .squad import Squad, SquadExists
from .platoon import Platoon
from .planetman import Planetman

class Operation:

    def __init__(self, name=None, start=None, end=None):

        self.name = name
        self.start = start
        self.end = end
        self.squads = {"alpha": None, 
                "bravo": None,
                "charlie": None,
                "delta": None}

    def __str__(self):

        return str(self.__dict__)

    def __repr__(self):

        return repr(self.__repr__)

    def create_squad(self, squad_name):

        '''
        Creates a squad and returns the squad object. Will raise an error if;
            Squad name is invalid
            Squad has already been created
        '''

        try:
            if isinstance(self.squads[squad_name], Squad):
                raise SquadExists
            else:
                self.squads[squad_name] = Squad()
                return self.squads[squad_name]
        except KeyError:
            InvalidSquad

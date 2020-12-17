from datetime import datetime

from .squad import Squad, SquadExists
from .platoon import Platoon

class Operation:

    def __init__(self):

        self.name = None
        self.start = None
        self.end = None
        self.squads = {"alpha": None, 
                "bravo": None,
                "charlie": None,
                "delta": None}

    def __str__(self):

        squads_present = ""
        for key, value in self.squads.items():
            if value is not None:
                squads_present += f"{key} "

        message = f"""Operation Name: {self.name}
                \tStart Time: {self.start}
                \tEnd Time: {self.end}
                \tSquads Present: {squads_present}"""

        return message



    def set_start(self, start):

        self.start = datetime.strptime(start, "%d/%m/%Y %H:%M")

    def set_end(self, end):

        self.end = datetime.strptime(end, "%d/%m/%Y %H:%M")

    def create_squad(self, squad_name):

        if self.squads[squad_name] is None:
            self.squads[squad_name] = Squad()
            return self.squads[squad_name]
        else:
            raise SquadExists

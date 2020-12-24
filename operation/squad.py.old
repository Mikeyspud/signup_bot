class Squad:

    def __init__(self):

        self.sl = None
        self.fl = None
        self.composition = None
        self.members = {}

    def __str__(self):

        message = f"""Squad Lead: {self.sl}
                    Fireteam Lead: {self.fl}
                    Composition: {self.composition}
                    Members:"""

        if self.members:
            for key, value in self.members.items():
                message += f"{key}: {value}"
        else:
            message += "Should probably get some friends"

        return message

    def set_comp(self, comp):

        self.composition = comp

    def add(self, name, role):

        if self.composition:
            if role in self.composition:
                if self.composition[role] == 0:
                    raise SquadCapacity()
                else:
                    self.composition[role] -= 1
            else:
                raise SquadRole()
        if name in self.members:
            self.remove(name)
        self.members[name] = role

    def remove(self, name):

        if name in self.members:
            if self.composition:
                role = self.members[name]
                self.composition[role] += 1
            del self.members[name]
        if name == self.sl:
            self.del_sl(name)
        if name == self.fl:
            self.del_fl(name)
#        else:
#            raise Exception("That member is not in the squad")

    def set_sl(self, name):

        self.sl = name

    def set_fl(self, name):

        self.fl = name

    def del_sl(self, name):

        self.sl = None

    def del_fl(self, name):

        self.fl = None

class SquadError(Exception):

    pass

class SquadExists(SquadError):

    pass

class SquadCapacity(SquadError):

    pass

class SquadRole(SquadError):

    pass

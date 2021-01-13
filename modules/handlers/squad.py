import discord
from . import errors, handler
from modules import settings

class Squad(handler.Handler):

    async def __call__(self):

        sub_commands = {"composition": self.composition,
                "sl": self.sl,
                "fl": self.fl}

        '''
        Extract the argument (args[1]) from the .create [squad] [argument] command
        and assign it to sub_command
        '''
        try:
            self.squad_name = self.args[0]
            sub_command = self.args[1]
        except:
            await self.help()
            await self.error(InvalidArguments, "Argument [ sl | fl | composition ] missing")

        '''
        If sub_command is not a valid command, inform the user
        '''
        if sub_command not in sub_commands:
            await self.help()
            await self.error(InvalidArguments, f"Argument {sub_command} is invalid")


        '''
        Check to see if an operatio has been initialised in the channel
        Inform the user if there is no operation
        '''
        try:
            operation_object = settings.operation_dict[self.channel_id]
        except KeyError:
            await self.error(NoOperationExists, "No operation exists in this channel")

        '''
        Checks if squad_name is valid in .create [squad_name] [argument].
        If not, inform the user
        '''
        if squad_name not in operation_object.squads:
            await self.help()
            await self.error(InvalidSquadName, f"Squad name {self.squad_name} is invalid")
        else:
            self.squad = operation_object.squads[self.squad_name]

        await sub_commands[sub_command]()

    async def composition(self):

        composition_arguments = self.args[3:]

        '''
        Check if composition_arguments is valid
        ie [role1, count1, role2, count2]

        There must be a role for every count
        '''

        if len(composition_arguments) % 2 != 0:
            await self.help()
            await self.error(InvalidComposition, f"Composition {composition_arguments} is invalid")

        composition = {}
        for index in range(0, len(composition_arguments), 2):
            role = composition_arguments(index)
            count = composition_arguments(index + 1)
            composition.update({role: count})

    async def sl(self):

        squad_lead = self.args[2]
        self.squad.sl = squad_leader

    async def fl(self):

        fireteam_lead = self.args[2]
        self.squad.fl = fireteam_lead

    async def help(self):

        embed = settings.help_embed()
        embed.add_field(name="Command:", 
                value="Allows a user to assign SL, FL and composition", 
                inline=False)
        embed.add_field(name=".squad [squad_name] sl [sl]",
                value='''Assigns [sl] as SL for squad [squad_name]. 
                If [sl] is not supplied, [sl] is set to the user who sent the message''',
                inline=False)
        embed.add_field(name=".squad [squad_name] fl [fl]",
                value='''Assigns [fl] as FL for squad [squad_name]. 
                If [fl] is not supplied, [fl] is set to the user who sent the message''', 
                inline=False)
        embed.add_field(name=".squad [squad_name] composition [composition", 
                value="Sets the composition of the squad", 
                inline=False)

        await self.user.send(embed=embed)


class InvalidArguments(errors.Error):

    def __init__(self, ctx, error):

        super().__init__(self, ctx, error)
        self.embed.add_field(name="Exception", value="handlers.squad.InvalidArguments", inline=False)


class NoOperationExists(errors.Error):

    def __init__(self, ctx, error):

        super().__init__(self, ctx, error)
        self.embed.add_field(name="Exception", value="handlers.squad.NoOperationExists", inline=False)


class InvalidSquadName(errors.Error):

    def __init__(self, ctx, error):

        super().__init__(self, ctx, error)
        self.embed.add_field(name="Exception", value="handlers.squad.InvalidSquadName", inline=False)


class InvalidComposition(errors.Error):

    def __init__(self, ctx, error):

        super().__init__(self, ctx, error)
        self.embed.add_field(name="Exception", value="handlers.squad.InvalidComposition", inline=False)

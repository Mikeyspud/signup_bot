import discord
from modules import settings
from . import errors, handler

class Add(handler.Handler):

    async def __call__(self):

        '''
        Check if operation in channel. If not, inform the user
        '''

        try:
            operation = settings.operation_dict[self.channel_id]
        except KeyError:
            await self.help()
            await self.error(NoOperationExists, "No operation exists")

        try:
            squad_name = self.args[0]
            role = self.args[1]
        except IndexError:
            await self.help()
            await self.error(InvalidArguments, "Invalid Arguments")

        if squad_name not in operation_object.squads:
            await self.help()
            await self.error(InvalidSquadName, "Invalid Squad Name")

        '''
        Check if role is an alias for another role
        '''

        '''
        alias_dict example

        {"HA": ["heavy", "ha"]}
        '''
        for key, alias_set in settings.alias_dict.items():
            if role in alias_dict[key]:
                role = key

        '''
        Checks the squad composition to see if it can accomodate
        the new addition
        '''

        if await functions.check_squad_composition(self.ctx, squad, role):
            squad.add(user.display_name, role)
            try:
                secondary_role = self.args[2]
                if secondary_role == "sl":
                    squad.sl == user.display_name

                if secondary_role == "fl":
                    squad.fl == user.display_name
            except IndexError:
                pass

    async def help(self):

        embed = settings.help_embed()
        embed.add_field(name="Command:", 
                value="Adds the user to the squad",
                inline=False)
        embed.add_field(name=".add [squad] [role] [ sl / fl (optional)]",
                value="Adds the user to [squad] as [role] plus [ sl / fl ]",
                inline=False)

        await self.user.send(embed=embed)


class NoOperationExists(self):

    def __init__(self, ctx, error):

        super().__init__(self, ctx, error)
        self.embed.add_field(name="Exception",
                value="handlers.add.NoOperationExists",
                inline=False)


class InvalidArguments(self):

    def __init__(self, ctx, error):

        super().__init__(self, ctx, error)
        self.embed.add_field(name="Exception",
                value="handlers.add.InvalidArguments",
                inline=False)

class InvalidSquadName(self):

    def __init__(self, ctx, error):

        super().__init__(self, ctx, error)
        self.embed.add_field(name="Exception",
                value="handlers.add.InvalidSquadName",
                inline=False)

import discord
from .. import settings, functions, operation                     # Global Variables
from . import errors, handler

class Create(handler.Handler):

    '''
    This command is used to create squads and operations

    Example:
        create squad alpha
        create operation [operation name]
    '''

    async def __call__(self):

        commands = {"operation": self.operation,
                "squad": self.squad}

        '''
        Check for args[0]
        '''
        try:
            sub_command = self.args[0]
        except IndexError:
            await self.help()

        '''
        Calls the respective function inside commands. If there is no respective function
        then run self.help()
        '''
        try:
            await commands[sub_command]()
        except KeyError:
            await self.help()

        functions.update_history_dict(self.channel_id, self.ctx.message.content)

    async def operation(self):

        try:
            operation_name = self.args[1]
        except IndexError:
            await self.help()

        if self.channel_id not in settings.operation_dict:
            settings.operation_dict[self.channel_id] = operation.Operation(name=operation_name)
            settings.embed_dict[self.channel_id] = {"op": None, "alpha": None, "bravo": None, "charlie": None, "delta": None}
        else:
            await self.error(OperationExists, "Operation aleady created")

    async def squad(self):

        try:
            squad_name = self.args[1]
        except:
            await self.help()

        if self.channel_id not in settings.operation_dict:
            await self.help()
            await self.error(NoOperationExists, "No operation exists")

        operation = settings.operation_dict[self.channel_id]
        if squad_name not in operation.squads:
            await self.help()
            await self.error(InvalidSquadName, "Squad name is invalid")
        elif operation.squads[squad_name] is not None:
            await self.help()
            await self.error(SquadExists, "Squad already exists")
        else:
            operation.create_squad(squad_name)

    async def help(self):

        embed = settings.help_embed()
        embed.add_field(name="Command:", 
                value="Allows a user to create an operation or a squad",
                inline=False)
        embed.add_field(name=".create operation [name]",
                value="Creates an operation in the channel called [name]",
                inline=False)
        embed.add_field(name=".create squad [squad_name]",
                value="Creates a squad for an operation in the channel",
                inline=False)

        await self.user.send(embed=embed)

class InvalidArguments(errors.Error):

    def __init__(self, ctx, error):

        errors.Error.__init__(self, ctx, error)
        self.embed.add_field(name="Exception", value="handlers.create.InvalidArguments", inline=False)

class InvalidSquadName(errors.Error):

    def __init__(self, ctx, error):

        errors.Error.__init__(self, ctx, error)
        self.embed.add_field(name="Exception", value="handlers.create.InvalidSquadName", inline=False)

class SquadExists(errors.Error):

    def __init__(self, ctx, error):

        errors.Error.__init__(self, ctx, error)
        self.embed.add_field(name="Exception", value="handlers.create.SquadExists", inline=False)

class OperationExists(errors.Error):

    def __init__(self, ctx, error):

        errors.Error.__init__(self, ctx, error)
        self.embed.add_field(name="Exception", value="handlers.create.OperationExistsArguments", inline=False)


class NoOperationExists(errors.Error):

    def __init__(self, ctx, error):

        errors.Error.__init__(self, ctx, error)
        self.embed.add_field(name="Exception", value="handlers.create.NoOperationExists", inline=False)

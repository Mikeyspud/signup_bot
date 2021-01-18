import discord
from .. import settings, functions, operation                     # Global Variables
from . import errors, handler


class Create(handler.Handler):

    '''
    Handles the 'create' command for the bot.
    Has parent class handler.Handler

    '.create' sub commands
    ---------------------

    'operation' : creates an operation
    'squad'     : creates a squad for an operation
    'help'      : sends a help embed to the author


    '.create' command-line parameters
    ---------------------
    '.create [sub_command]'

    'sub_command';
        'operation' will result in Create.operation()
        being called.

        'squad' will result in Create.squad() being
        called.

        'help' will result in Create.help() being
        called.
    '''

    async def __call__(self):

        commands = {"operation": self.op,
                    "squad": self.squad,
                    "help": self.help}

        try:
            sub_command = self.args[0]
        except IndexError:
            await self.help()

        try:
            await commands[sub_command]()
        except KeyError:
            await self.help()
            await self.error(InvalidArguments,
                             f"{sub_command} is invalid argument")

        '''
        We want to save each create command as it is called
            so that it can be later saved as a template
        '''
        functions.update_history_dict(
            self.channel_id, self.ctx.message.content)

    async def op(self):

        '''
        sub_command 'operation' for '.create' command.
            Creates an operation.Operation object.

            Stores the Operation object in a global dict
            with the key as the discord channel_id.
            (settings.operation_dict[self.channel_id])

        '.create operation' command-line parameters
        -------------------
        '.create operation [name]';

            'name': defines Operation.name
        '''

        try:
            operation_name = self.args[1]
        except IndexError:
            await self.error(MissingArguments, "Missing argument [name]")
            await self.help()

        if self.channel_id not in settings.operation_dict:
            self._create_operation(operation_name)
            self._create_embed_entries()
        else:
            await self.error(OperationExists, "Operation aleady created")

    def _create_operation(self, operation_name):

        settings.operation_dict[self.channel_id] = operation.Operation(
                name=operation_name)

    def _create_embed_entries(self):

        settings.embed_dict[self.channel_id] = {
                "op": None, "alpha": None, "bravo": None, "charlie": None, "delta": None}

    async def squad(self):

        '''
        sub_command 'squad' for '.create' command.
            Creates an operation.Squad object within
            the created operation.Operation.squads[squad_name]
            attribute

        '.create squad' command-line parameters
        -----------------
        '.create squad [name]';

            'name': defines name of squad. Must be same
                as key within Operation.squads.
        '''

        try:
            squad_name = self.args[1]
        except BaseException:
            await self.help()

        if self.operation is None:
            await self.help()
            await self.error(NoOperationExists, "No operation exists")

        if squad_name not in self.operation.squads:
            await self.help()
            await self.error(InvalidSquadName, "Squad name is invalid")
        elif self.operation.squads[squad_name] is not None:
            await self.help()
            await self.error(SquadExists, "Squad already exists")
        else:
            self.operation.create_squad(squad_name)

    async def help(self):

        embed = settings.help_embed()
        embed.add_field(
            name="Command:",
            value="Allows a user to create an operation or a squad",
            inline=False)
        embed.add_field(
            name=".create operation [name]",
            value="Creates an operation in the channel called [name]",
            inline=False)
        embed.add_field(
            name=".create squad [squad_name]",
            value="Creates a squad for an operation in the channel",
            inline=False)

        await self.user.send(embed=embed)


class InvalidArguments(errors.Error):

    pass


class InvalidSquadName(errors.Error):

    pass


class SquadExists(errors.Error):

    pass


class OperationExists(errors.Error):

    pass


class NoOperationExists(errors.Error):

    pass


class InvalidPermissions(errors.Error):

    pass

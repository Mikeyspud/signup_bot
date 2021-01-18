import discord
from modules import settings
from . import errors, handler


class Remove(handler.Handler):

    async def __call__(self):

        '''
        Check if operation is created. Inform the user
        if not
        '''

        try:
            operation = settings.operation_dict[self.channel_id]
        except KeyError:
            await self.help()
            await self.error(NoOperationExists, "No operation exists")

        '''
        Validate arguments
        '''
        try:
            squad_name = self.args[0]
        except BaseException:
            await self.help()
            await self.error(InvalidArguments, "Invalid Arguments")

        try:
            squad = operation.squads[squad_name]
            squad.remove(user.display_name)
        except KeyError:
            await self.help()
            await self.error(InvalidSquadName, "Invalid Squad name")

    async def help(self):

        embed = settings.help_embed()
        embed.add_field(name="Command:",
                        value="Allows a user to remove themselves from squad",
                        inline=False)
        embed.add_field(name=".remove [squad]",
                        value="Removes user from squad [squad]",
                        inline=False)

        await self.user.send(embed=embed)


class NoOperationExists(errors.Error):

    pass


class InvalidArguments(errors.Error):

    pass


class InvalidSquadName(errors.Error):

    pass

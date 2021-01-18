import sys
from modules import settings                         # Global Variables
import discord                          # Discord API

from . import errors, handler


class Show(handler.Handler):

    '''
    This command is used to extract information from the database
        and post it to the discord

    Example:
        show template [name]
    '''

    async def __call__(self):

        '''
        function:
            looks at the "show" command argument (args[0]) and then call
            the respective function
        '''

        show_dict = {"template": self.template,         # if args[0] is "template, call self.template
                     "help": self.help}                 # if args[0] is "help", call the self.help

        try:
            sub_command = self.args[0]
        except BaseException:
            await self.help()
            await self.error(InvalidArguments, "No arguments supplied")

        full_command = show_dict[sub_command]
        await full_command()

    async def template(self):

        message = ""

        cursor = settings.op_collection.find({}, {"_id": False})
        for document in cursor:
            message += f"{document}\n"
        await self.ctx.channel.send(message)

    async def help(self):

        embed = settings.help_embed()
        embed.add_field(
            name="Command:",
            value="Allows a user to retrieve data from the database",
            inline=False)
        embed.add_field(
            name=".show template [template name]",
            value="Retrieves template from database\nOptional:\n- [template_name]",
            inline=True)

        await self.user.send(embed=embed)


class InvalidArguments(errors.Error):

    pass

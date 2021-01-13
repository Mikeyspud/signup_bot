import sys
from modules import settings                         # Global Variables
import discord                          # Discord API

from . import errors, handler

class Close(handler.Handler):

    def __init__(self, ctx, client, *args):

        handler.Handler.__init__(self, ctx, args)
        self.client = client

    async def __call__(self):

        try:
            sub_command = self.args[0]
        except:
            pass

        if sub_command == "help":
            await self.help()
        elif sub_command:
            await self.help()
            await self.error()

        try:
            del operation_dict[channel_id]
        except KeyError:
            pass

        for message_id in settings.embed_dict[self.channel_id]:
            channel = await self.client.get_channel(channel_id)
            message = await channel.fetch_message(message_id)
            await client.delete_message(message)

        try:
            del embed_dict[channel_id]
        except KeyError:
            pass

        try:
            del history_dict[channel_id]
        except KeyError:
            pass

    async def help(self):

        embed = settings.helf_embed()
        embed.add_field(name="Command:", value="Allows the user to close an operation in a channel", inline=False)

class InvalidArguments(errors.Error):

    def __init__(self, ctx, error):

        errors.Error.__init__(self, ctx, error)
        self.embed.add_field(name="Exception", value="handlers.show.InvalidArguments", inline=False)

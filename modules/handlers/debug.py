import discord
from modules import settings
from . import errors, handler

class Debug(handler.Handler):

    async def __call__(self):

        '''
        Returns debug information
        '''

        try:
            debug_messages = [f"settings.operation_dict[self.channel_id]}",
                    f"history_dict {settings.history_dict[self.channel_id]}",
                    f"embed_dict {settings.embed_dict[self.channel_id]}",
                    f"alias_dict {settings.alias_dict}"]

            for debug_message in debug_messages:
                await ctx.send(debug_message)

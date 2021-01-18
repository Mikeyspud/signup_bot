import discord                  # discord API
from .. import settings                 # global variables


class Error(Exception):

    def __init__(self, ctx, error):

        self.ctx = ctx
        self.error = error
        self.user = ctx.message.author
        self.channel_id = ctx.channel.id
        self.embed = settings.debug_embed()
        self.embed.add_field(name="Triggering message",
                             value=self.ctx.message.content,
                             inline=False)
        self.embed.add_field(name="Channel ID",
                             value=self.channel_id,
                             inline=False)
        self.embed.add_field(name="Error",
                             value=self.error,
                             inline=False)
        self.embed.add_field(name="Exception",
                             value=self._classname(),
                             inline=False)

    def _classname(self):

        cls = type(self)
        module = cls.__module__
        name = cls.__qualname__
        if module is not None and module != "__builtin__":
            name = module + "." + name
        return name

    async def debug(self):

        await self.user.send(embed=self.embed)

import discord
from modules import settings
from . import errors, handler

class Load(handler.Handler):

    async def __call__(self):

        try:
            template_name = args[0]
        except IndexError:
            await self.help()
            await self.error(InvalidArguments, "Supplied Invalid Arguments")

        template = settings.op_collection.find_one({template_name: {'$exists': True}}, 
                {'_id': False})

        if len(template) == 0:
            await self.help()
            await self.error(NoTemplate, f"There is no template called {template_name}")
        else:
            await self.install_template(template[template_name])

    async def install_template(self, template):

        for full_command in template:
            command = full_command.split(" ")[:1][0][1:]
            positional_arg = full_command.split(" ")[1:]
            command = client.get_command(command)
            await command(self.ctx, *positional_arg)

    async def help(self):

        embed = settings.help_embed()
        embed.add_field(name="Command:", 
                value="Allows a user to load a saved template",
                inline=False)
        embed.add_field(name=".load [template_name]", 
                value="Loads template called [template_name]",
                inline=False)
        embed.add_field(name="How to show templates",
                value=".show template [optional template name (leave blank for all)]",
                inline=False)

        await self.user.send(embed=embed)

class InvalidArguments(errors.Error):

    def __init__(self, ctx, error):

        errors.Error.__init__(self, ctx, error)
        self.embed.add_field(name="Exception", value="handlers.load.InvalidArguments", inline=False)

class NoTemplate(errors.Error):

    def __init__(self, ctx, error):

        errors.Error.__init__(self, ctx, error)
        self.embed.add_field(name="Exception", value="handlers.load.NoTemplate", inline=False)
